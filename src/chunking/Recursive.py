class Recursive:
    def __init__(
            self,
            separators: tuple = ("\n\n", "\n", ". ", " ", ""),
            chunk_size: int = 100,
            chunk_overlap: int = 20,
    ) -> None:
        self._separators = separators
        self._chunk_size = chunk_size
        self._chunk_overlap = chunk_overlap
        if self._chunk_overlap >= self._chunk_size:
            raise ValueError(f"chunk_overlap ({self._chunk_overlap}) must be smaller than chunk size ({self._chunk_size})")
        if self._chunk_size <= 0:
            raise ValueError(f"chunk_size ({self._chunk_size}) must be large and positive")
    def split_text(self, text: str, separators: tuple) -> list[str]:
        if separators is None:
            separators = self._separators

        separator = separators[0]
        chunked = text.split(separator
                             )
        chunks = []
        current_chunk = ""

        for piece in chunked:
            if len(piece) > self._chunk_size:
                if current_chunk:
                    chunks.append(current_chunk)
                    current_chunk = ""
                sub_chunks = self.split_text(piece, separators[1:])
                chunks.extend(sub_chunks)
                continue
            if current_chunk:
                chosen = current_chunk + separator + piece
            else:
                chosen = piece

            if len(chosen) <= self._chunk_size:
                current_chunk = chosen
            else:
                chunks.append(current_chunk)
                overlap_text = current_chunk[-self._chunk_overlap:] if current_chunk else ""
                current_chunk = overlap_text + separator + piece if overlap_text else piece

        if current_chunk:
            chunks.append(current_chunk)
        return chunks
test_text = (
    "The history of computing spans many decades of steady progress. "
    "Early machines filled entire rooms and required teams of engineers "
    "just to keep them running. Over time, transistors replaced vacuum "
    "tubes, and integrated circuits made it possible to pack enormous "
    "computing power into much smaller devices. Personal computers "
    "brought this power into homes and offices, changing how people "
    "worked, communicated, and shared information. Later, the rise of "
    "the internet connected these machines into a single global network, "
    "enabling instant communication and access to vast amounts of "
    "information from almost anywhere in the world."
)
print(len(test_text))
chunker = Recursive(chunk_size = 100, chunk_overlap = 20, separators = ("\n\n", "\n", ". ", " ", ""))
chunks = chunker.split_text(test_text, separators = ("\n\n", "\n", ". ", " ", ""))
for i, chunk in enumerate(chunks):
    print(f"Chunk {i}: [{chunk}]")
    print(f"Length: {len(chunk)}\n")