"""A class representing a single Document.
Contains an optional Annotation, and a list of fields."""

from typing import List, Dict

from .Annotation import Annotation


class Document:

    """A class representing a single Document.
    Contains an optional Annotation, and a list of fields.
    """

    def __init__(
        self,
        structured_fields: List[Dict] = None,
        annotation: Annotation = None,
        document_index: int = None,
    ):
        """Create a new document.

        Args:
            structured_fields (List[Dict], optional): List of fields.
            annotation (Annotation, optional): The Annotation of the textual
               part of this document (such as annotations over the short text)
            document_index (None): When set, this is useful when splitting the
              documents into sentences. The document_index is the index of the
              original document that this sentence came from.
        """
        super().__init__()
        self.fields = structured_fields
        self.annotation = annotation
        self.document_index = document_index

    def to_dict(self):
        """Return a dict of this Document.

        Returns:
            dict: A dictionary representing this document.
        """
        return {
            "fields": self.fields,
            "annotations": self.annotation.to_dict()
            if self.annotation
            else None,
        }

    def split_sentences(self, delimiter):
        """Split this document into sentences, i.e. a list of Documents
        that have been split by the given delimiter.

        Args:
            delimiter (str): The delimiter to use.

        Returns:
            List[Document]: List of documents.
            List[Relation]: List of relations that were removed due to being
              across multiple sentences.
        """

        new_docs = []
        sent_tokens = []

        sent_start_idx = 0
        sent_end_idx = 0

        removed_relations = []
        seen_rels = set()

        for i, token in enumerate(self.annotation.tokens):
            if token != delimiter:
                sent_tokens.append(token)

            if token == delimiter or i == (len(self.annotation.tokens) - 1):
                sent_end_idx = i
                if i == len(self.annotation.tokens) - 1:
                    sent_end_idx = i + 1

                sent_mentions = []
                sent_mention_ids = {}

                # Rebuild the list of mentions in this sentence
                for m in self.annotation.mentions:
                    if (m.start < sent_start_idx) or (m.end > sent_end_idx):
                        continue

                    m_dict = m.to_dict()
                    m_dict["start"] = m_dict["start"] - sent_start_idx
                    m_dict["end"] = m_dict["end"] - sent_start_idx
                    sent_mentions.append(m_dict)
                    sent_mention_ids[m] = len(sent_mentions) - 1

                # Rebuild the list of relations in this sentence
                # Discard any cross-sentence relations (whose start or end do
                # not lie within this sentence)
                # print('-------')
                sent_relations = []
                for r in self.annotation.relations:
                    # print(
                    #     r,
                    #     r.start.start,
                    #     r.end.start,
                    #     sent_start_idx,
                    #     sent_end_idx,
                    # )
                    if (
                        (r.start.start < sent_start_idx)
                        or (r.end.start > sent_end_idx)
                        or (r.start.start > sent_end_idx)
                        or (r.end.start < sent_start_idx)
                    ):
                        continue

                    seen_rels.add(r)
                    r_dict = r.to_dict()
                    # print(sent_mention_ids)
                    r_dict["start"] = sent_mention_ids[r.start]
                    r_dict["end"] = sent_mention_ids[r.end]
                    sent_relations.append(r_dict)

                new_ann = Annotation(
                    tokens=sent_tokens,
                    mentions=sent_mentions,
                    relations=sent_relations,
                )

                new_docs.append(Document(self.fields, new_ann))

                sent_tokens = []
                sent_mentions = []
                sent_relations = []

                sent_start_idx = i + 1

        for r in self.annotation.relations:
            if r not in seen_rels:
                removed_relations.append(r)

        return new_docs, removed_relations

    def __str__(self):
        return str(self.to_dict())
