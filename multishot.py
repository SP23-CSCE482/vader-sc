multi_shot_primer = {}
multi_shot_key = {}
multi_shot_comment = {}
multi_shot_comment_end = {}
multi_shot_primer["DOCSTYLE"] = '''
SAMPLE 1
CODE:
void getInput(string names[], int ages[], const int SIZE) {
    // for each student
    for (int i = 0; i < SIZE; i++) {
        // prompt and store the name of the current student
        cout << "Enter the name for student #" << i + 1 << ": ";
        getline(cin, names[i]);

        // prompt and store for the age of the current student
        cout << "Enter the age for student #" << i + 1 << ": ";
        cin >> ages[i];

        // need to ignore the newline for the next iteration
        cin.ignore();
    }
}
CODE_END

COMMENT:
/*******************************************************************************
* 
*   Use a for loop to prompt the user for the name/age of each student. Store
*   the information in the appropriate array.
*
* Inputs:
*   names - a string array for storing the students' names
*   ages  - an integer array for storing the students' ages
*   SIZE  - a constant integer that represents the size of the two arrays
*******************************************************************************/
COMMENT_END

SAMPLE 2
CODE:
::is_sorted_backward(it_index itx_first, it_index itx_last)
{
    size_t nblock = size_t(itx_last - itx_first);
    range_it rng = get_group_range(*itx_first, nblock);

    size_t nelem = rng.size();
    size_t min_process = (std::max)(BLOCK_SIZE, (nelem >> 3));

    size_t nsorted2 = bsc::number_stable_sorted_backward(rng.first, rng.last,
                                                         min_process, cmp);
    if (nsorted2 == nelem) return true;
    if (nsorted2 == 0 ) return false;
    Iter_t itaux = rng.last - nsorted2;
    size_t nsorted1 = nelem - nsorted2;

    if (nsorted1 <= (BLOCK_SIZE << 1))
    {
        flat_stable_sort(rng.first, itaux, cmp, ptr_circ);
        bscu::insert_sorted_backward(rng.first, itaux, rng.last, cmp,
                                     ptr_circ->get_buffer());
    }
    else
    {   // Adjust the size of nsorted2 for to be a number of blocks
        size_t nblock1 = (nsorted1 + BLOCK_SIZE - 1) >> Power2;
        size_t nsorted1_adjust = (nblock1 << Power2);
        flat_stable_sort(rng.first, rng.first + nsorted1_adjust, cmp,
                         ptr_circ);
        merge_range_pos(itx_first, itx_first + nblock1, itx_last);
    };
    return true;
};
CODE_END

COMMENT:
/*******************************************************************************
* 
*   This function checks if a range of elements is sorted in a descending order.
*   It uses the number_stable_sorted_backward function to determine the number
*   of sorted elements in the range, and then uses the flat_stable_sort and
*   insert_sorted_backward functions to sort the remaining elements.
*
* Inputs:
*   itx_first - an iterator pointing to the first element in the range
*   itx_last  - an iterator pointing to the last element in the range
*
* Outputs:
*   bool - true if the range is sorted in a descending order, false otherwise
*******************************************************************************/
COMMENT_END

SAMPLE 3
CODE:

'''
multi_shot_key["DOCSTYLE"] = '''SAMPLE 3
CODE:''' 

multi_shot_comment["DOCSTYLE"] = '''
CODE_END

COMMENT:'''

multi_shot_comment_end["DOCSTYLE"] = '''COMMENT_END''' 


#
#
# CPP
#
#
multi_shot_primer["CPP.DOCSTRING.AI"] = '''
SAMPLE 1
CODE:
void getInput(string names[], int ages[], const int SIZE) {
    // for each student
    for (int i = 0; i < SIZE; i++) {
        // prompt and store the name of the current student
        cout << "Enter the name for student #" << i + 1 << ": ";
        getline(cin, names[i]);

        // prompt and store for the age of the current student
        cout << "Enter the age for student #" << i + 1 << ": ";
        cin >> ages[i];

        // need to ignore the newline for the next iteration
        cin.ignore();
    }
}
CODE_END

COMMENT:
// This is a function called `getInput` that takes in three parameters: an array of strings called `names`, an array of integers called `ages`, and a constant integer called `SIZE`.
COMMENT_END

SAMPLE 2
CODE:
::is_sorted_backward(it_index itx_first, it_index itx_last)
{
    size_t nblock = size_t(itx_last - itx_first);
    range_it rng = get_group_range(*itx_first, nblock);

    size_t nelem = rng.size();
    size_t min_process = (std::max)(BLOCK_SIZE, (nelem >> 3));

    size_t nsorted2 = bsc::number_stable_sorted_backward(rng.first, rng.last,
                                                         min_process, cmp);
    if (nsorted2 == nelem) return true;
    if (nsorted2 == 0 ) return false;
    Iter_t itaux = rng.last - nsorted2;
    size_t nsorted1 = nelem - nsorted2;

    if (nsorted1 <= (BLOCK_SIZE << 1))
    {
        flat_stable_sort(rng.first, itaux, cmp, ptr_circ);
        bscu::insert_sorted_backward(rng.first, itaux, rng.last, cmp,
                                     ptr_circ->get_buffer());
    }
    else
    {   // Adjust the size of nsorted2 for to be a number of blocks
        size_t nblock1 = (nsorted1 + BLOCK_SIZE - 1) >> Power2;
        size_t nsorted1_adjust = (nblock1 << Power2);
        flat_stable_sort(rng.first, rng.first + nsorted1_adjust, cmp,
                         ptr_circ);
        merge_range_pos(itx_first, itx_first + nblock1, itx_last);
    };
    return true;
};
CODE_END

COMMENT:
// This is a function called `is_sorted_backward` that takes in two iterators `itx_first` and `itx_last` representing a range of elements and checks if the range is sorted in non-increasing order.
COMMENT_END

SAMPLE 3
CODE:

'''
multi_shot_key["CPP.DOCSTRING.AI"] = '''SAMPLE 3
CODE:''' 

multi_shot_comment["CPP.DOCSTRING.AI"] = '''
CODE_END

COMMENT:'''

multi_shot_comment_end["CPP.DOCSTRING.AI"] = '''COMMENT_END''' 

#
#
# Python
#
#

multi_shot_primer["PY.DOCSTRING.AI"] = '''
SAMPLE 1
CODE:
def list_reverse(arr,size):
 
    #if only one element present, then return the array
    if(size==1):
        return arr
     
    #if only two elements present, then swap both the numbers.
    elif(size==2):
        arr[0],arr[1],=arr[1],arr[0]
        return arr
     
    #if more than two elements presents, then swap first and last numbers.
    else:
        i=0
        while(i<size//2):
 
    #swap present and preceding numbers at time and jump to second element after swap
            arr[i],arr[size-i-1]=arr[size-i-1],arr[i]
       
    #skip if present and preceding numbers indexes are same
            if((i!=i+1 and size-i-1 != size-i-2) and (i!=size-i-2 and size-i-1!=i+1)):
                arr[i+1],arr[size-i-2]=arr[size-i-2],arr[i+1]
            i+=2
        return arr
CODE_END

COMMENT:
# This is a Python function called `list_reverse` that takes in two parameters: `arr` (an array) and `size` (an integer). The function reverses the order of the elements in the array in place and returns the reversed array.
COMMENT_END

SAMPLE 2
CODE:
    def twoSum(self, nums, target):
        # two point
        nums_index = [(v, index) for index, v in enumerate(nums)]
        nums_index.sort()
        begin, end = 0, len(nums) - 1
        while begin < end:
            curr = nums_index[begin][0] + nums_index[end][0]
            if curr == target:
                return [nums_index[begin][1], nums_index[end][1]]
            elif curr < target:
                begin += 1
            else:
                end -= 1
                
CODE_END

COMMENT:
# This is a function called `addTwoNumbers` that takes in two linked lists `l1` and `l2` representing non-negative integers in reverse order (i.e. the ones digit is at the head of the list). The function adds the two numbers and returns the sum as a linked list in reverse order.
COMMENT_END

SAMPLE 3
CODE:

'''
multi_shot_key["PY.DOCSTRING.AI"] = '''SAMPLE 3
CODE:''' 

multi_shot_comment["PY.DOCSTRING.AI"] = '''
CODE_END

COMMENT:'''

multi_shot_comment_end["PY.DOCSTRING.AI"] = '''COMMENT_END''' 


#
#
# Java
#
#

multi_shot_primer["JAVA.DOCSTRING.AI"] = '''
SAMPLE 1
CODE:
    public int lengthOfLongestSubstring(String s) {
    	int[] charMap = new int[256];
    	Arrays.fill(charMap, -1);
    	int i = 0, maxLen = 0;
    	for (int j = 0; j < s.length(); j++) {
    		if (charMap[s.charAt(j)] >= i) {
    			i = charMap[s.charAt(j)] + 1;
    		}
    		charMap[s.charAt(j)] = j;
    		maxLen = Math.max(j - i + 1, maxLen);
    	}
    	return maxLen;
    }
CODE_END

COMMENT:
// This is a method that takes a string `s` as input and returns an integer representing the length of the longest substring without repeating characters.
COMMENT_END

SAMPLE 2
CODE:
    public boolean isPalindrome(int x) {
        if (x < 0) return false;
        int div = 1;
        while ( x / div >= 10) {
            div *= 10;
        }
        while (x !=0) {
            int l = x / div;
            int r = x % 10;
            if (l != r) return false;
            // Remove left and right number
            x = (x % div) / 10;
            div /= 100;
        }
        return true;
    }
                
CODE_END

COMMENT:
// This is a method that takes an integer `x` as input and returns a boolean value indicating whether `x` is a palindrome or not. A palindrome is a number that reads the same backward as forward.
COMMENT_END

SAMPLE 3
CODE:

'''
multi_shot_key["JAVA.DOCSTRING.AI"] = '''SAMPLE 3
CODE:''' 

multi_shot_comment["JAVA.DOCSTRING.AI"] = '''
CODE_END

COMMENT:'''

multi_shot_comment_end["JAVA.DOCSTRING.AI"] = '''COMMENT_END''' 



multi_shot_primer["NOSHOT"] = '''
CODE:

'''
multi_shot_key["NOSHOT"] = '''
CODE:''' 

multi_shot_comment["NOSHOT"] = '''
CODE_END

COMMENT:'''

multi_shot_comment_end["NOSHOT"] = '''COMMENT_END''' 



multi_shot_primer["EMOJI"] = '''
SAMPLE 1
CODE:
void getInput(string names[], int ages[], const int SIZE) {
    // for each student
    for (int i = 0; i < SIZE; i++) {
        // prompt and store the name of the current student
        cout << "Enter the name for student #" << i + 1 << ": ";
        getline(cin, names[i]);

        // prompt and store for the age of the current student
        cout << "Enter the age for student #" << i + 1 << ": ";
        cin >> ages[i];

        // need to ignore the newline for the next iteration
        cin.ignore();
    }
}
CODE_END

COMMENT:
//Use a for loop 🔄 to prompt 📺 ⌨️ the user 🤓  for the name 🫥/age 👴 of each student 🧑‍🎓. Store the information 💾 in the appropriate array 📦.
COMMENT_END

SAMPLE 2
CODE:
::is_sorted_backward(it_index itx_first, it_index itx_last)
{
    size_t nblock = size_t(itx_last - itx_first);
    range_it rng = get_group_range(*itx_first, nblock);

    size_t nelem = rng.size();
    size_t min_process = (std::max)(BLOCK_SIZE, (nelem >> 3));

    size_t nsorted2 = bsc::number_stable_sorted_backward(rng.first, rng.last,
                                                         min_process, cmp);
    if (nsorted2 == nelem) return true;
    if (nsorted2 == 0 ) return false;
    Iter_t itaux = rng.last - nsorted2;
    size_t nsorted1 = nelem - nsorted2;

    if (nsorted1 <= (BLOCK_SIZE << 1))
    {
        flat_stable_sort(rng.first, itaux, cmp, ptr_circ);
        bscu::insert_sorted_backward(rng.first, itaux, rng.last, cmp,
                                     ptr_circ->get_buffer());
    }
    else
    {   // Adjust the size of nsorted2 for to be a number of blocks
        size_t nblock1 = (nsorted1 + BLOCK_SIZE - 1) >> Power2;
        size_t nsorted1_adjust = (nblock1 << Power2);
        flat_stable_sort(rng.first, rng.first + nsorted1_adjust, cmp,
                         ptr_circ);
        merge_range_pos(itx_first, itx_first + nblock1, itx_last);
    };
    return true;
};
CODE_END

COMMENT:
//This function 🔨 checks ✅ if a range 🏔️ of elements 🔥💧🌱 is sorted in a descending order🚶. It uses the number_stable_sorted_backward function 🔨 to determine the number 💯 of sorted elements 🔥💧🌱 in the range 🏔️, and then uses the flat_stable_sort 🗝️ and insert_sorted_backward 🗝️ functions 🔨 to sort the remaining elements  🔥💧🌱.
COMMENT_END

SAMPLE 3
CODE:

'''
multi_shot_key["EMOJI"] = '''SAMPLE 3
CODE:''' 

multi_shot_comment["EMOJI"] = '''
CODE_END

COMMENT:'''

multi_shot_comment_end["EMOJI"] = '''COMMENT_END'''

multi_shot_primer["LITE"] = '''
SAMPLE 1
CODE:
void getInput(string names[], int ages[], const int SIZE) {
    // for each student
    for (int i = 0; i < SIZE; i++) {
        // prompt and store the name of the current student
        cout << "Enter the name for student #" << i + 1 << ": ";
        getline(cin, names[i]);

        // prompt and store for the age of the current student
        cout << "Enter the age for student #" << i + 1 << ": ";
        cin >> ages[i];

        // need to ignore the newline for the next iteration
        cin.ignore();
    }
}
CODE_END

COMMENT:
/*******************************************************************************
* 
*   Use a for loop to prompt the user for the name/age of each student. Store
*   the information in the appropriate array.
*
* Inputs:
*   names - a string array for storing the students' names
*   ages  - an integer array for storing the students' ages
*   SIZE  - a constant integer that represents the size of the two arrays
*******************************************************************************/
COMMENT_END

SAMPLE 2
CODE:

'''

multi_shot_key["LITE"] = '''SAMPLE 2
CODE:'''

multi_shot_comment["LITE"] = '''
CODE_END

COMMENT:'''

multi_shot_comment_end["LITE"] = '''COMMENT_END'''
