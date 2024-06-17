from Bio import pairwise2
from Bio.Seq import Seq

def color_highlight(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"

def show_alignment(seq1, seq2, width=50):
    alignments = pairwise2.align.globalxx(Seq(seq1), Seq(seq2), one_alignment_only=True)
    
    # Taking the first alignment (if available)
    if alignments:
        a1, a2, score, begin, end = alignments[0]
        
        highlighted_a1 = []
        highlighted_a2 = []
        
        a1_part = ""
        a2_part = ""    
        
        for i in range(len(a1)):
            if a1[i] == a2[i]:
                # Yellow background color code '43'
                a1_part += color_highlight(a1[i], "43")
                a2_part += color_highlight(a2[i], "43")
            else:
                a1_part += a1[i]
                a2_part += a2[i]
                
            if (i + 1) % width == 0:
                highlighted_a1.append(a1_part)
                highlighted_a2.append(a2_part)
                a1_part = ""
                a2_part = ""
        
        highlighted_a1.append(a1_part)
        highlighted_a2.append(a2_part)
        
        for i in range(len(highlighted_a1)):
            if i == len(highlighted_a1) - 1:
                print(highlighted_a1[i], '<- Sequence 1')
                print(highlighted_a2[i], '<- Sequence 2')
                break
            print(highlighted_a1[i])
            print(highlighted_a2[i])
            print()
            
    else:
        print("No alignment found.")
        
        
if __name__ == "__main__":
    print('■■■■■■■■■■■■■■■■■■■■ Sequence Alignment Tool ■■■■■■■■■■■■■■■■■■■■')
    target = input('Sequence 1: ')
    query = input('Sequence 2: ')
    print('■■■■■■■■■■■■■■■■■■■■■■■■■■■■ Result! ■■■■■■■■■■■■■■■■■■■■■■■■■■■■')
    show_alignment(target, query)