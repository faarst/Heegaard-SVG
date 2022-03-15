
def sewOnto(A,B,progressReport=False):

    # check error stuff

    # skip sewOnto when either A or B is empty
    if len(A)==0:
        print('sewOnto(A,B) ERROR: A=[]');
        return
    if len(B)==0:
        print('sewOnto(A,B) skipped since B=[]');
        return

    # check that a and b both have length 1 mod 3
    if len(A)%3!=1:
        print('sewOnto(A,B) ERROR: len(A) mod 3 should be 1');
        print('len(A)='+str(len(A)));
        return
    if len(B)%3!=1:
            print('sewOnto(A,B) ERROR: if len(B)!=0, len(B) mod 3 should be 1');
            print('len(B)='+str(len(B)));
            return

    # check that a and b are lists of two-element lists
    for x in A:
        if len(x)!=2:
            print('sewOnto(A,B) ERROR: element A['+str(A.index(x))+'] has wrong length');
            print(x);
            return
    for x in B:
        if len(x)!=2:
            print('sewOnto(A,B) ERROR: element B['+str(B.index(x))+'] has wrong length');
            print(x);
            return

    # check that neither A nor B is "already a loop"
    if A[0]==A[-1]:
        print('sewOnto(A,B) ERROR: element A is a loop');
        print(A);
        return
    if B[0]==B[-1]:
        print('sewOnto(A,B) ERROR: element B is a loop');
        print(B);
        return

    # check that one of the endpts of B matches A[-1], and reverse B if needed
    if B[0]!=A[-1]:
        B.reverse();
        if progressReport==True: print('new B is '+str(B));
    if B[0]!=A[-1]:
        print('neither B endpoint matches A[-1]');
        return

    # if no problems have been detected, sew B onto the end of A (don't repeat the joining pt)
    A.extend(B[1:]);

    # print out the result (if progressReport="True")
    if progressReport==True: print('sewing complete; now A='+str(A));
    return A;



def bezMaker(X):

    # check that the preBez input X has length 1 mod 3
    if len(X)%3!=1:
        print('the preBez input has the wrong length (should be 1 mod 3)');
        print('length='+str(len(X)));
        return

    # make the string
    bezString = 'M '+str(X[0][0])+','+str(X[0][1]);
    for i in range((len(X)-1)/3):
        bezString = bezString+' C '+str(X[3*i+1][0])+','+str(X[3*i+1][1]);
        bezString = bezString+' '+str(X[3*i+2][0])+','+str(X[3*i+2][1]);
        bezString = bezString+' '+str(X[3*i+3][0])+','+str(X[3*i+3][1]);
        (i)

    # return the bezier string as output
    return bezString


# scratch stuff:

#A = [[0,1],[2,3],[4,5],[6,7]];
#B = [[0,1],[2,3],[4,5],[6,7]];

#asdf = bezMaker(sewOnto(A,B));
#print asdf;




