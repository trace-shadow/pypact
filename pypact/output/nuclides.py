from pypact.output.serializable import Serializable
from pypact.output.nuclide import Nuclide
from pypact.output.tags import NUCLIDES_HEADER
import pypact.util.propertyfinder as pf
from pypact.util.lines import first_occurrence

NUCLIDES_IGNORES = ['\n', '|']


class Nuclides(Serializable):
    """
        The nuclides type from the output
    """
    def __init__(self):
        self.nuclides = []

    def json_deserialize(self, j):
        super(Nuclides, self).json_deserialize(j)
        self.json_deserialize_list(j, 'nuclides', Nuclide)

    def fispact_deserialize(self, filerecord, interval):

        self.__init__()

        substring = filerecord[interval]

        header_index, header_line = first_occurrence(lines=substring, tag=NUCLIDES_HEADER)

        nuclidetag = 'TOTAL NUMBER OF NUCLIDES PRINTED IN INVENTORY'

        def nr_of_nuclides():
            number = pf.first(datadump=substring,
                              headertag=NUCLIDES_HEADER,
                              starttag=nuclidetag,
                              endtag='',
                              ignores=NUCLIDES_IGNORES,
                              asstring=False)
            return int(number)

        # The column headers line is after the main nuclide header
        def get_header(index):
            raw = substring[index].split('  ')
            header = list(filter(''.__ne__, raw))
            for ignore in NUCLIDES_IGNORES:
                if ignore in header:
                    header = list(filter(ignore.__ne__, header))

            return header

        # The nuclides list starts from the line prior to the total number
        # so we need the line number of this tag and count backwards
        i, line = first_occurrence(lines=substring, tag=nuclidetag)
        if i < 0:
            return

        for n in range(i - nr_of_nuclides(), i):
            nuclide = Nuclide()
            nuclide.fispact_deserialize(substring[n:], column_headers=get_header(i - nr_of_nuclides()-3))
            self.nuclides.append(nuclide)
