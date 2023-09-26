"""A class that stores documents in Mention format."""

from typing import List

from .Mention import Mention
from .Relation import Relation

from .size_limits import MAX_SENT_LENGTH, MAX_WORD_LENGTH

import logging as logger


class Annotation(object):
    """An Annotation for the textual portion of a Document.
    Contains a list of tokens, a list of mentions,
    a list of relations."""

    def __init__(
        self,
        tokens: list,
        mentions: list,
        relations: list = None,
    ):
        """Create a new Annotation.

        Args:
            tokens (list): The list of tokens of the document.
            mentions (list): The list of mentions of the document. Each
               mention must follow the correct format ('start', 'end',
               'mentions'/'entities', 'labels'/'type').
            relations (list, optional): The list of relations of the
               document. Each relation must follow the correct format
               ('start'/'head', 'end'/'tail', 'type').
        """
        super(Annotation, self).__init__()
        self.tokens = tokens
        self._mention_ids_map = {}
        self.mentions = self._parse_mentions(mentions, tokens)
        if relations:
            self.relations = self._parse_relations(relations)
        else:
            self.relations = None

    def to_dict(self):
        """Return a dictionary representation of this Annotation.
        Format will be similar to the input dataset.

        Returns:
            dict: Dictionary representation of this Annotation.
        """
        return {
            "tokens": self.tokens,
            "mentions": [m.to_dict() for m in self.mentions],
            "relations": [r.to_dict() for r in self.relations]
            if self.relations
            else None,
        }

    def _parse_mentions(self, mentions, tokens):
        """Parse a list of mentions (which should each be stored as a dict).
        Ignore duplicate mentions i.e. mentions with the same start,
        end, and label.
        Each dict must have the format
           {"start": <int>, "end": <int>, "labels": List[str],
            "tokens": List[str]}

        Args:
            mentions (list): A list of dicts where each dict
              corresponds to a mention. Each dict must have 'start', 'end'
              and 'labels' keys.
            tokens (list): A list of tokens (i.e. the sentence).

        Returns:
            list: A list of Mention objects.
        """
        seen_mentions = set()
        mentions_list = []

        # Maintain a mapping from the mention id (in the original data)
        # to the id of the mention in the list of parsed Mentions,
        # so that relations can be correctly created.
        self._mention_ids_map = {}

        for i, m in enumerate(mentions):
            try:
                m_obj = Mention(
                    m["start"],
                    m["end"],
                    tokens[m["start"] : m["end"]],
                    m["labels"] if "labels" in m else [m["type"]],
                    i,
                )
                self._mention_ids_map[i] = m_obj
            except KeyError as e:
                logger.error(
                    f"Could not parse document due to "
                    "missing keys. The 'mentions' key of each document must "
                    "have 'start', 'end', 'tokens', and either 'labels' "
                    "or 'type'."
                )

            if str(m_obj) not in seen_mentions:
                mentions_list.append(m_obj)
            seen_mentions.add(str(m_obj))

        return mentions_list

    def _parse_relations(self, relations) -> List[Relation]:
        """Parse a given list of relations (which each should be a dict)
        and return a list of Relation objects.

        Args:
            relations (list): A list of relations. Each relation should
               have the keys 'start', 'end', and 'type'.

        Returns:
            List[Relation]: The parsed list of Relations.
        """

        relations_list = []
        _mention_ids_map = self._mention_ids_map
        for r in relations:
            start_key = "start" if "start" in r else "head"
            end_key = "end" if "end" in r else "tail"
            try:
                r_obj = Relation(
                    _mention_ids_map[r[start_key]],
                    _mention_ids_map[r[end_key]],
                    r["type"],
                )
                relations_list.append(r_obj)
            except KeyError as e:
                raise KeyError(
                    f"Could not parse relations of document "
                    "due to missing keys. The 'relations' key of each "
                    "document must have 'start'/'head', 'end'/'tail', "
                    "and 'type'."
                )
            except IndexError as e:
                raise IndexError(
                    f"Could not parse relations of document "
                    " because the mention corresponding to the relation with "
                    f" start: {r['start']} and end: {r['end']} was not found."
                )
            except ValueError as e:
                raise ValueError(
                    f"Could not parse relations of document "
                    f"due to the following error:\n{e}"
                )

        return relations_list

    def flatten(self):
        """Flatten this doc, i.e. ensure each mention only has one label."""
        for m in self.mentions:
            m.labels = [m.get_first_label()]
            if m.labels is None:
                del m

    @staticmethod
    def from_dict(d: dict):
        """Create an Annotation from a dictionary.

        Args:
            d (dict): The dictionary. Must contain,
            tokens, mentions, relations.

        Returns:
            Annotation: An Annotation.

        Raises:
            ValueError: If the dictionary is missing a required
            key.
        """

        # Validate things such as max word length, sent length, etc,
        # before attempting to create Annotation object
        if any(len(t) > MAX_WORD_LENGTH for t in d["tokens"]):
            word = ""
            for t in d["tokens"]:
                if len(t) > MAX_WORD_LENGTH:
                    word = t
            raise ValueError(
                f"Word must be at most {MAX_WORD_LENGTH} characters "
                f"long: {word}"
            )
        if len(d["tokens"]) > MAX_SENT_LENGTH:
            raise ValueError(
                f"Sentence must contain at most {MAX_SENT_LENGTH} words."
            )

        mention_key = "mentions"
        if "mentions" not in d:
            mention_key = "entities"
            if "entities" not in d:
                raise ValueError(
                    "Could not parse document as it does not have "
                    "a 'mentions' or an 'entities' key."
                )

        try:
            annotation = Annotation(
                tokens=d["tokens"],
                mentions=d[mention_key],
                relations=d["relations"],
            )
        except KeyError as e:
            print(d)
            raise ValueError(
                "Dictionary must contain tokens, mentions, and relations."
            )

        return annotation

    def __repr__(self):
        """Represent this document as a string.

        Returns:
            str: String representation of this document.
        """
        mens_str = (
            "\n  ".join([str(m) for m in self.mentions])
            if self.mentions
            else "-"
        )
        rels_str = (
            "\n  ".join([str(r) for r in self.relations])
            if self.relations
            else "-"
        )
        return "Tokens: %s\nMentions:  \n  %s\nRelations: \n  %s\n" % (
            " ".join(self.tokens),
            mens_str,
            rels_str,
        )
