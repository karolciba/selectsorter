"""Creates delatage that will lazy sort large list based on slice query.

Uses combination of quickselects to slice large list to obtain unsorted
slice according to the query. Then uses python sort to sort the slice.
On average should achieve O(N*ML

Use quickselect algoritm to return just k-th sorted element from unsorted list.

Follows generator protocol, each time quickseleting one next element from
unsorted list.

Usage

    sortee = sorted(large_list)
    # sortee is a delegate that will lazy sort on slice

    print "Top 30 elements", sortee[0:30]

"""

class qsorted(object):
    def __init__(self, orig_list):
        """Creates object answering to adressing single in sorted place elements
        or small slices of list. Assumes large size of list and therefore doing
        sorting in place.
        """
        # TODO: check if fully_sorted, if so do nothing
        # TODO: keep list of sorted chunks to speed up consecutive calls
        self._list = orig_list
    def _quickselect(self, key, left_bound=0, right_bound=None):
        """Selects and puts on position k-th element of sorted list"""
        # TODO: possibly reimplement in C (using Cython?)
        while True:
            pivot = self._list[left_bound]
            left_pointer = left_bound + 1
            right_bound = right_bound or (len(self._list) - 1)
            right_pointer = right_bound
            while True:
                while self._list[left_pointer] < pivot and left_pointer < right_bound:
                    left_pointer += 1
                while self._list[right_pointer] >= pivot and right_pointer > left_bound:
                    right_pointer -= 1

                if left_pointer >= right_pointer:
                    break

                # swap elements
                self._list[left_pointer], self._list[right_pointer] = \
                    self._list[right_pointer], self._list[left_pointer]

            # swap pivot and iteration stop
            self._list[left_bound], self._list[right_pointer] = \
                self._list[right_pointer], self._list[left_bound]

            # element sorted into requested position
            if right_pointer == key:
                # print "Found"
                return self._list[key]
            elif key < right_pointer:
                # tail-recurse into left part
                right_bound = left_pointer
            # element must be on right side
            else:
                # tail-recurse into right part
                left_bound = left_pointer

    def __getitem__(self, key):
        """sorted[key] -> item at x position in sorted list
        sorted[slice] -> sorted slice of elemented from list

        Due to O(N) nature of QuickSelect algoritm it will be optimal to
        ask for small slices (in comparison to size of list), otherwise
        performance will be degraded to builtin sorted function
        """
        if isinstance(key, slice):
            start = key.start or 0
            stop = key.stop or len(self._list) - 1
            # put right bound on position
            right = self._quickselect(stop)
            # put left bound on position
            # all x in the middle will be x > left and x < right
            left = self._quickselect(start, right_bound = stop)
            # so take what's inside and sort it falling back to req. impl.
            self._list[key] = sorted(self._list[key])
            return self._list[key]
        else:
            return self._quickselect(key)

    def __iter__(self):
        def iter():
            for i in xrange(0,len(self._list)-1):
                yield self._quickselect(i, left_bound = i)
        return iter()

if __name__ == "__main__":
    import random

    print("Poor man's testsuite")

    size = 10000

    random_list = [ 9, 2, 1, 3, 3, 0, 8, 4, 5, 6, 7]
    sort = qsorted(random_list)

    assert sort[3:6] == [3, 3, 4]

    size = 1000000
    fro, to = 0, 300
    norm_random_list = range(0,size)
    random.shuffle(norm_random_list)
    # norm_random_list = [ random.randint(0,1000000) for _ in xrange(size) ]
    test_random_list = norm_random_list[:]


    def regular():
        part = sorted(norm_random_list)[fro:to]

    def tested():
        part = qsorted(norm_random_list, False)
        sort = part[fro:to]
