class Fixed:
    def __init__(
            self,
            chunk_size: int,
            chunk_overlap: int,
    )->None:
        self._chunk_size = chunk_size
        self._chunk_overlap = chunk_overlap
        if self._chunk_overlap >= self._chunk_size:
            raise ValueError(f"chunk_overlap ({self._chunk_overlap}) must be smaller than chunk size ({self._chunk_size})")
        if self._chunk_size <= 0:
            raise ValueError(f"chunk_size ({self._chunk_size}) must be large and positive")

    @property
    def chunk_size(self) -> int:
        return self._chunk_size
    @property
    def chunk_overlap(self) -> int:
        return self._chunk_overlap

    def split_text(
            self,
            text: str,
    )-> list[str]:
        start = 0
        end = self._chunk_size
        chunks = []
        step = self._chunk_size - self._chunk_overlap
        while start < len(text):
            chunked = text[start:end]
            chunks.append(chunked)
            start = start + step
            end = start + self._chunk_size


        return chunks


edge_case_text = ("Rapidly rapidity revolves round the redundant rodents")
print(len(edge_case_text))
chunker = Fixed(chunk_size = 100, chunk_overlap = 20)
chunks = chunker.split_text(edge_case_text)
for i, chunk in enumerate(chunks):
    print(f"Chunk {i}: [{chunk}]")
    print(f"Length: {len(chunk)}\n")


"""Mid-word cuts — Chunk 0 ends mid-word ("...rooms a", cut before finishing "and"),
 and Chunk 3 similarly ends "...this pow" mid-word. This is correct for fixed-size 
 chunking specifically — it's supposed to be naive and ignore word boundaries.
This is actually useful for your README later: you can point at this exact
 output as evidence of why fixed-size is the weakest baseline, compared to
  your recursive/semantic methods which will respect these boundaries."""