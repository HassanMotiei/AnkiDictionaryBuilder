from ankidict.core.models import DictionaryEntry
from ankidict.logger import setup_logger
from tqdm import tqdm

logger = setup_logger()

class DictionaryEngine:

    COMMIT_INTERVAL = 1000

    def __init__(self):
        self.importer = None
        self.parser = None

    def load(self, importer, parser):

        self.importer = importer
        self.parser = parser

    def process_all(self):

        iterator = self.importer

        if hasattr(iterator, "__len__"):

            iterator = tqdm(
                iterator,
                total=len(iterator),
                desc="Importing",
                unit="word",
            )

        else:

            iterator = tqdm(
                iterator,
                desc="Importing",
                unit="word",
            )

        for raw in iterator:
            yield self.parser.parse(raw)

    def build_database(self, repository):

        count = 0

        try:

            for entry in self.process_all():

                repository.save(entry)

                count += 1

                if count % self.COMMIT_INTERVAL == 0:

                    repository.commit()

                    logger.info("%,d entries processed", count)

            repository.commit()

            logger.info("Finished: %,d entries.", count)

        finally:

            repository.close()