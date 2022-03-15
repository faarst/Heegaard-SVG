

## note: this is written for python 2.7


###################################################
##  CHANGES FROM V4:
###################################################

# SVG output filenames will now include t (and hex/fin if necessary)
# vertical spacing is a little different (try to make hexagons nicer)
# change at line tag "blYdefn"
# change at line tag "midYdefn"
# added "bulbCenter" T/F option
# added "yCushion" option

# this list above may be incomplete!

# NOTE: both V4 and V5 will fail (self-int beta) when there is a large difference between any t[i] and t[i+1]


###################################################
## keep function definitions in separate file in same directory:
###################################################

from bezFunctions import sewOnto
from bezFunctions import bezMaker

###################################################
## user input
###################################################

t = [3,-4,1,5,-3];
gridX = 60;
gridY = 50;
widA = 12;
widB = 8;
strokeWidth = 1;
zwRad = 5;
bgColor = 'none';  # background color.  'none' is an option
tGap = 2;
sGap = 1;
hexagons = True;
aGap = 1.8;    # scales radius of alpha curve near basepoint
bulbCenter = True;    # centers first and last basepoint inside beta bulbs
bulbWidth = 2*widA;
yCushion = 3;    # extra space on top and bottom; will be re-defined to 1 if no hex regions in diagram

###################################################
## prep stuff
###################################################

T = [abs(twistCoeff) for twistCoeff in t];
tSign = [t[i]/T[i] for i in range(len(t))];
swaps = [1 if tSign[i]!=tSign[i+1] else 0 for i in range(len(t)-1)];     # marks sign changes btwn consec twists
if hexagons==False or max(swaps)==0:        # no need for extra cushion if no hexagons in diagram
    yCushion = 1;
blY = max(T)+yCushion;                            # blYdefn            # baseline Y value (where a-arcs live)
dimX = (2*sum(T)+len(T)*tGap+sum(swaps)*sGap);
dimY = 2*blY;

###################################################
## locate basepoints and spiral start pts
###################################################

zwPos = [T[0],T[0]+tGap];        # this will list the x-positions of the z/w basepoints
midLR = [];                   # this will mark the starting x-positions for the spirals bL and bR
for i in range(len(t)-1):
    midLR.append(zwPos[-1]+T[i]);                    # mark new "left midpoint" on i^th alpha curve
    midLR.append(zwPos[-1]+T[i]+sGap*swaps[i]);         # mark new "right midpoint" ...
    zwPos.append(zwPos[-1]+T[i]+T[i+1]+sGap*swaps[i]);  # mark new z/w pt at right of i^th alpha
    zwPos.append(zwPos[-1]+tGap);                       # mark new z/w pt at left of next alpha
(i)

###################################################
## describe b-arcs
## (un-scaled, will scale by gridX later)
###################################################

bL = [];
bLdir = [];
for i in range(len(t)-1):
    newPts = [midLR[2*i]];
    newDirs = [(t[i]/T[i])*(T[i]+1)];
    for j in range(T[i]):                 # for bR it will be T[i+1] everywhere
        newPts.append(newPts[-1]-(2*T[i]-2*j+tGap-1)*(-1)**(j));
        newDirs.append((t[i]/T[i])*(-1)**(j+1)*(T[i]-j));    # might need adjustment here!
        (j)
    bL.append(newPts);
    bLdir.append(newDirs);
    (i)

bR = [];
bRdir = [];
for i in range(len(t)-1):
    newPts = [midLR[2*i+1]];
    newDirs = [(-1)*(t[i+1]/T[i+1])*(T[i+1]+1)];
    for j in range(T[i+1]):
        newPts.append(newPts[-1]+(2*T[i+1]-2*j+tGap-1)*(-1)**(j));
        newDirs.append((t[i+1]/T[i+1])*(-1)**(j)*(T[i+1]-j));    # might need adjustment here!
        (j)
    bR.append(newPts);
    bRdir.append(newDirs);
    (i)


###################################################
##        scale up to gridX and gridY
###################################################

zwPos = [position*gridX for position in zwPos];
midLR = [position*gridX for position in midLR];
blY   = blY*gridY;
dimX  = dimX*gridX;
dimY  = dimY*gridY;

###################################################
##        generate alpha-curve bezier path strings
###################################################

alphaBez = [];

for i in range(len(t)-1):
    newPath = "M "+str(zwPos[2*i+1])+","+str(blY+widA);
    newPath = newPath+" C "+str(zwPos[2*i+1]+aGap*widA)+","+str(blY+widA);
    newPath = newPath+" "+str(zwPos[2*i+2]-aGap*widA)+","+str(blY+widA);
    newPath = newPath+" "+str(zwPos[2*i+2])+","+str(blY+widA);
    newPath = newPath+" C "+str(zwPos[2*i+2]+aGap*widA)+","+str(blY+widA);
    newPath = newPath+" "+str(zwPos[2*i+2]+aGap*widA)+","+str(blY-widA);
    newPath = newPath+" "+str(zwPos[2*i+2])+","+str(blY-widA);
    newPath = newPath+" C "+str(zwPos[2*i+2]-aGap*widA)+","+str(blY-widA);
    newPath = newPath+" "+str(zwPos[2*i+1]+aGap*widA)+","+str(blY-widA);
    newPath = newPath+" "+str(zwPos[2*i+1])+","+str(blY-widA);
    newPath = newPath+" C "+str(zwPos[2*i+1]-aGap*widA)+","+str(blY-widA);
    newPath = newPath+" "+str(zwPos[2*i+1]-aGap*widA)+","+str(blY+widA);
    newPath = newPath+" "+str(zwPos[2*i+1])+","+str(blY+widA);
    alphaBez.append(newPath);
    (i)

###################################################
##        generate pre-bezier list of points [x,y] for beta curves
###################################################

preBezLOuter = [];
preBezLCap = [];
preBezLInner = [];
preBezROuter = [];
preBezRCap = [];
preBezRInner = [];
preBezMOuter = [];
preBezMInner = [];

for i in range(len(t)-1):

    xL = [x*gridX for x in bL[i]];
    yL = [y*gridY for y in bLdir[i]];
    xR = [x*gridX for x in bR[i]];
    yR = [y*gridY for y in bRdir[i]];

    # add entry i to preBezLOuter
    newThang = [[xL[0]+widB,blY]];
    # outbound
    for j in range(1,len(xL)):
        #from V1: newThang.append([xL[j-1]-(-1)**j*widB,blY+yL[j-1]-(-1)**(j)*widB*tSign[i]]);
        newThang.append([xL[j-1]-(-1)**j*widB,blY+yL[j-1]-(-1)**(j)*widB*tSign[i]]);
        newThang.append([xL[j]+(-1)**j*widB,blY+yL[j-1]-(-1)**(j)*widB*tSign[i]]);
        newThang.append([xL[j]+(-1)**j*widB,blY]);
        (j)
    preBezLOuter.append(newThang);

    # add entry i to preBezLInner
    newThang = [[xL[0]-widB,blY]];
    # inbound
    for j in range(1,len(xL)-1):    # <-- change here since V2
        #from V1: newThang.append([xL[j-1]+(-1)**j*widB,blY+yL[j-1]+(-1)**(j)*widB*tSign[i]]);
        newThang.append([xL[j-1]+(-1)**j*widB,blY+yL[j-1]+(-1)**(j)*widB*tSign[i]]);
        newThang.append([xL[j]-(-1)**j*widB,blY+yL[j-1]+(-1)**(j)*widB*tSign[i]]);
        newThang.append([xL[j]-(-1)**j*widB,blY]);
        (j)
    # bulbous part
    jj = len(xL)-1;
    newThang.append([xL[jj-1]+(-1)**jj*widB,blY+yL[jj-1]+(-1)**(jj)*widB*tSign[i]]);
    newThang.append([xL[jj]-(-1)**jj*bulbWidth,blY+yL[jj-1]+(-1)**(jj)*widB*tSign[i]]);  #####################################
    newThang.append([xL[jj]-(-1)**jj*bulbWidth,blY]);                                    #####################################
    preBezLInner.append(newThang);

    # add entry i to preBezLCap
    newThang = [];
    newThang.append(preBezLOuter[-1][-1]);
    newThang.append([preBezLOuter[-1][-1][0],preBezLOuter[-1][-1][1]+(yL[-1]/abs(yL[-1]))*2*(widA+widB)]);
    newThang.append([preBezLInner[-1][-1][0],preBezLInner[-1][-1][1]+(yL[-1]/abs(yL[-1]))*2*(widA+widB)]);
    newThang.append(preBezLInner[-1][-1]);
    preBezLCap.append(newThang);

    # add entry i to preBezROuter
    newThang = [[xR[0]-widB,blY]];
    # outbound
    for j in range(1,len(xR)):
        #from V1: newThang.append([xR[j-1]+(-1)**j*widB,blY+yR[j-1]+(-1)**(j)*widB*tSign[i+1]]);
        newThang.append([xR[j-1]+(-1)**j*widB,blY+yR[j-1]+(-1)**(j)*widB*tSign[i+1]]);
        newThang.append([xR[j]-(-1)**j*widB,blY+yR[j-1]+(-1)**(j)*widB*tSign[i+1]]);
        newThang.append([xR[j]-(-1)**j*widB,blY]);
        (j)
    preBezROuter.append(newThang);

    # add entry i to preBezRInner
    newThang = [[xR[0]+widB,blY]];
    # inbound
    for j in range(1,len(xR)-1):    # <-- change here since V2
        #from V1: newThang.append([xR[j-1]-(-1)**j*widB,blY+yR[j-1]-(-1)**(j)*widB*tSign[i+1]]);
        newThang.append([xR[j-1]-(-1)**j*widB,blY+yR[j-1]-(-1)**(j)*widB*tSign[i+1]]);
        newThang.append([xR[j]+(-1)**j*widB,blY+yR[j-1]-(-1)**(j)*widB*tSign[i+1]]);
        newThang.append([xR[j]+(-1)**j*widB,blY]);
        (j)
    # bulbous part
    jj = len(xR)-1;
    newThang.append([xR[jj-1]-(-1)**jj*widB,blY+yR[jj-1]-(-1)**(jj)*widB*tSign[i+1]]);
    newThang.append([xR[jj]+(-1)**jj*bulbWidth,blY+yR[jj-1]-(-1)**(jj)*widB*tSign[i+1]]);
    newThang.append([xR[jj]+(-1)**jj*bulbWidth,blY]);
    preBezRInner.append(newThang);

    # add entry i to preBezRCap
    newThang = [];
    newThang.append(preBezROuter[-1][-1]);
    newThang.append([preBezROuter[-1][-1][0],preBezROuter[-1][-1][1]+(yR[-1]/abs(yR[-1]))*2*(widA+widB)]);
    newThang.append([preBezRInner[-1][-1][0],preBezRInner[-1][-1][1]+(yR[-1]/abs(yR[-1]))*2*(widA+widB)]);
    newThang.append(preBezRInner[-1][-1]);
    preBezRCap.append(newThang);

    # add entries i to preBezMOuter and preBezMInner if needed, else append []
    if swaps[i]==1:
        # the new entry for preBezMOuter
        newThang = [];
        newThang.append(preBezLInner[i][0]);
        newThang.append([preBezLInner[i][0][0],blY-tSign[i]*(2*gridY+widB)]);
        newThang.append([preBezRInner[i][0][0],blY-tSign[i]*(2*gridY+widB)]);
        newThang.append(preBezRInner[i][0]);
        preBezMOuter.append(newThang);
        # the new entry for preBezMInner
        newThang = [];
        newThang.append(preBezLOuter[i][0]);
        newThang.append([preBezLOuter[i][0][0],blY-tSign[i]*(2*gridY-widB)]);
        newThang.append([preBezROuter[i][0][0],blY-tSign[i]*(2*gridY-widB)]);
        newThang.append(preBezROuter[i][0]);
        preBezMInner.append(newThang);
    else:
        preBezMOuter.append([]);
        preBezMInner.append([]);

    (i)

###################################################
##        option: tweak the first and last basepoint posisions (center within beta bulbs)
###################################################

if bulbCenter==True:
    zwPos[0] = (preBezLOuter[0][-1][0]+preBezLInner[0][-1][0])/2;
    zwPos[-1] = (preBezROuter[-1][-1][0]+preBezRInner[-1][-1][0])/2;

###################################################
##        generate bezier strings for beta curves
###################################################

betaBez = [];

for i in range(len(t)-1):

    # if twist sign change, do finger move OR leave hexagon (user option hex)
    if swaps[i]==1:
        if hexagons:
            midX = (midLR[2*i]+midLR[2*i+1])/2;
            midY = gridY*tSign[i]*(max(T[i],T[i+1])+2);        # midYdefn
            w = tSign[i]*widB;
            dx = max(T[i],T[i+1])*gridX;
            preBezLOuter[i][0:2] = [[midX,blY+midY+w],[midX-dx,blY+midY+w]];
            preBezLInner[i][0:2] = [[midX,blY+midY-w],[midX-dx,blY+midY-w]];
            preBezROuter[i][0:2] = [[midX,blY+midY+w],[midX+dx,blY+midY+w]];
            preBezRInner[i][0:2] = [[midX,blY+midY-w],[midX+dx,blY+midY-w]];
            newPreBez = preBezLOuter[i];
            sewOnto(newPreBez,preBezLCap[i]);
            sewOnto(newPreBez,preBezLInner[i]);
            sewOnto(newPreBez,preBezRInner[i]);
            sewOnto(newPreBez,preBezRCap[i]);
            sewOnto(newPreBez,preBezROuter[i]);
        else:
            newPreBez = preBezLOuter[i];
            sewOnto(newPreBez,preBezLCap[i]);
            sewOnto(newPreBez,preBezLInner[i]);
            sewOnto(newPreBez,preBezMOuter[i]);
            sewOnto(newPreBez,preBezRInner[i]);
            sewOnto(newPreBez,preBezRCap[i]);
            sewOnto(newPreBez,preBezROuter[i]);
            sewOnto(newPreBez,preBezMInner[i]);
    # if no sign change, just L and R parts
    else:
        newPreBez = preBezLOuter[i];
        sewOnto(newPreBez,preBezLCap[i]);
        sewOnto(newPreBez,preBezLInner[i]);
        sewOnto(newPreBez,preBezROuter[i]);
        sewOnto(newPreBez,preBezRCap[i]);
        sewOnto(newPreBez,preBezRInner[i]);

    # make sure it's a loop
    if newPreBez[-1]!=newPreBez[0]:
        print('WARNING: beta_'+str(i)+' is not a loop');

    #convert to string and then append to betaBez
    newBetaString = bezMaker(newPreBez);
    betaBez.append(newBetaString);
    (i)




###################################################
##  make the svg file (GENUS 0 HEEGAARD DIAGRAM)
###################################################

if max(swaps)==0:
    svgLabel = 'P'+str(t)+'.svg';
elif hexagons==True:
    svgLabel = 'P'+str(t)+'hex.svg';
else:
    svgLabel = 'P'+str(t)+'fin.svg';

f = open(svgLabel,'w');


f.write('<svg xmlns="http://www.w3.org/2000/svg"\n');
f.write('     xmlns:xlink="http://www.w3.org/1999/xlink"\n');
f.write('     width="'+str(dimX)+'px"\n');
f.write('     height="'+str(dimY)+'px">\n');

# optional background color
if bgColor!='none':
    f.write('<rect width="'+str(dimX)+'" height="'+str(dimY)+'" fill="'+bgColor+'"/>');

# add the alpha curves
f.write('<g stroke="red" fill="none" stroke-width="'+str(strokeWidth)+'">\n');
for i in range(len(t)-1):
    f.write('     <path d="'+alphaBez[i]+'"/>\n');
    (i)
f.write('</g>\n');

# add the beta curves
f.write('<g fill="none" stroke-width="'+str(strokeWidth)+'">\n');
for i in range(len(t)-1):
    if i%2==0:
        f.write('     <path stroke="blue" d="'+betaBez[i]+'"/>\n');
    else:
        f.write('     <path stroke="darkblue" d="'+betaBez[i]+'"/>\n');
    (i)
f.write('</g>\n');

# add circles for z points
f.write('<g fill="black">\n');
for i in range(len(t)):
    f.write('     <circle cx="'+str(zwPos[2*i+1])+'" cy="'+str(blY)+'" r="'+str(zwRad)+'"/>\n');
    (i)
f.write('</g>\n');


# add circles for w points
f.write('<g fill="black">\n');
for i in range(len(t)):
    f.write('     <circle cx="'+str(zwPos[2*i])+'" cy="'+str(blY)+'" r="'+str(zwRad)+'"/>\n');
    (i)
f.write('</g>\n');

f.write('</svg>');





###################################################
##        output stuff
###################################################

#
# print();
