import io,glob,os,struct,codecs,shutil,zlib

def handlePackC(fl,fullpackname,idoffsetvalue):
    packfslslength, = struct.unpack('<Q',fl.read(0x8))
    packfslsoffset = fl.tell()
    packfslslength += packfslsoffset

    files,fileblocksize,null1,null2 = struct.unpack('<4I',fl.read(0x10))

    for i in range(files):
        number,null2,offset = struct.unpack('<2IQ',fl.read(0x10))
        print(number)
        
        offset += idoffsetvalue
        size, = struct.unpack('<Q',fl.read(0x8))
        null = fl.read(0x10)
        packfslsbreak = fl.tell()

        fullname = GENESTRT(fl,packfslslength,number)
        packname = "pack/"+ "fs.apk" + "/"
        packname += fullname
        packname += ".apk"

        print(packname+':'+hex(offset)+'|'+hex(size))
        

        export(fl,fl.tell(),fullpackname,packname,offset,0,size)
        fl.seek(packfslsbreak)

def handlePackA(fl,fullpackname):
    '''
    packtoclength, = struct.unpack('<Q',fl.read(0x8))
    packtocoffset = fl.tell()
    packtoclength += packtocoffset
    fileblocksize, = struct.unpack('<Q',fl.read(0x8))
    offset,null = struct.unpack('<2I',fl.read(0x8))
    fl.seek(packtoclength)
    '''

    #idstring = fl.read(8) # "PACKTOC "
    packfslslength, = struct.unpack('<Q',fl.read(0x8))
    packfslsoffset = fl.tell()
    packfslslength += packfslsoffset

    plus,allfiles,null3 = struct.unpack('<2IQ',fl.read(0x10))
    startoffset = fl.tell()
    null0,number,null3 = struct.unpack('<2IQ',fl.read(0x10))
    offsetvalue, = struct.unpack('<I',fl.read(0x4))
    offsetvalue *= plus
    offsetvalue += startoffset

    nextFiles, = struct.unpack('<I',fl.read(0x4))
    null3 = fl.read(0x10)

    #print(number)
    #input('')

    #if number == 1:
    #    number = 0

    if number == 2:
        number = 0

    #breakpoint = fl.tell()
    fl.seek(packfslslength)

    idstring = fl.read(8) # "PACKFSLS"

    genesrtlength, = struct.unpack('<Q',fl.read(0x8))
    geneoffset = fl.tell()
    genesrtlength += geneoffset

    packname = GENESTRT(fl,genesrtlength,number)
    packname += "/"
    tmpname = packname
    fl.seek(offsetvalue)

    getfoldername(fl,packname,fullpackname,plus,startoffset,genesrtlength,nextFiles)

def getfoldername(fl,packname,fullpackname,plus,startoffset,genesrtlength,files):

    for i in range(files):
        null,number,null3 = struct.unpack('<2IQ',fl.read(0x10))

        if null in [0x200,0]:
            breakfilename = fl.tell()
            filename = GENESTRT(fl,genesrtlength,number)
            fl.seek(breakfilename)

            tmpname = packname
            packname += filename

            offset,size,zsize = struct.unpack('<3Q',fl.read(0x8*3))            
            export(fl,fl.tell(),fullpackname,packname,offset,zsize,size)
            packname = tmpname
            
        else:
            fileoffsetvalue, = struct.unpack('<I',fl.read(0x4))
            fileoffsetvalue *= plus
            fileoffsetvalue += startoffset

            nextFiles, = struct.unpack('<I',fl.read(0x4))
            null3 = fl.read(0x10)
            breakpoint = fl.tell()

            foldername = GENESTRT(fl,genesrtlength,number)
        
            fl.seek(fileoffsetvalue)
            filejudge, = struct.unpack('<I',fl.read(0x4))
            fl.seek(fileoffsetvalue)

            if filejudge in [0x0,0x200]:
                foldername += "/"
                tmpname = packname
                packname += foldername
                getfilename(fl,packname,fullpackname,plus,startoffset,genesrtlength,nextFiles)
            elif filejudge in [0x1]:
                foldername += "/"
                tmpname = packname
                packname += foldername
                getfoldername(fl,packname,fullpackname,plus,startoffset,genesrtlength,nextFiles)
            else:
                print('filejudge1:'+hex(filejudge))
                input('')

            packname = tmpname
            fl.seek(breakpoint)

def getfilename(fl,packname,fullpackname,plus,startoffset,genesrtlength,files):

    for i in range(files):
        null,number,null3 = struct.unpack('<2IQ',fl.read(0x10))

        if null in [0x0,0x200]:
            breakfilename = fl.tell()
            filename = GENESTRT(fl,genesrtlength,number)
            fl.seek(breakfilename)

            tmpname = packname
            packname += filename

            offset,size,zsize = struct.unpack('<3Q',fl.read(0x8*3))
            export(fl,fl.tell(),fullpackname,packname,offset,zsize,size)
            packname = tmpname

        else:
            fileoffsetvalue1, = struct.unpack('<I',fl.read(0x4))
            fileoffsetvalue1 *= plus
            fileoffsetvalue1 += startoffset

            nextFiles, = struct.unpack('<I',fl.read(0x4))
            null3 = fl.read(0x10)
            breakpoint1 = fl.tell()

            foldername = GENESTRT(fl,genesrtlength,number)
            
            fl.seek(fileoffsetvalue1)
            filejudge1, = struct.unpack('<I',fl.read(0x4))
            fl.seek(fileoffsetvalue1)

            if filejudge1 in [0x0,0x200]:
                foldername += "/"
                tmpname = packname
                packname += foldername
                getfilename(fl,packname,fullpackname,plus,startoffset,genesrtlength,nextFiles)
            elif filejudge1 in [0x1]:
                foldername += "/"
                tmpname = packname
                packname += foldername
                getfoldername(fl,packname,fullpackname,plus,startoffset,genesrtlength,nextFiles)
            else:
                print('filejudge2:'+hex(filejudge1))
                input('')

            packname = tmpname
            fl.seek(breakpoint1)

def export(fl,breakpoint,filename,name,offset,zsize,size):
    '''
    dirname = os.path.dirname(name)
    basename,extname = os.path.splitext(filename)
        
    if os.path.isdir(dirname) == False:
        os.makedirs(dirname)

    fl.seek(offset)
    new = open(name,'wb')

    if zsize != 0:
        new.write(zlib.decompress(fl.read(zsize)))
    else:
        new.write(fl.read(size))

    new.close()
    '''

    
    idx = codecs.open(basename+'.txt','ab','utf16')
    idx.write(str(name)+','+hex(offset)+','+hex(zsize)+','+hex(size))
    idx.write('\r\n')
    idx.close()

    #print(name+':'+hex(offset)+'|'+hex(zsize)+'|'+hex(size))

    fl.seek(breakpoint)
    
def test_scr(fl):
    start = fl.tell()
    #print(start)
    test2, = struct.unpack('<B',fl.read(1))
    
    while test2 != 0:
        test2, = struct.unpack('<B',fl.read(1))
        
    end = fl.tell()
    #end -= 1
    size = end
    size -= start
    fl.seek(start)
    script = fl.read(size).decode('cp932').rstrip('\x00')
    script = script.replace('\n','\\n')
    #print(script)
    #end += 1
    return script,end


def GENESTRT(fl,genesrtlength,number):
    fl.seek(genesrtlength)
    idstring = fl.read(8) # GENESTRT
    #print(idstring)
    geneeoflength, = struct.unpack('<Q',fl.read(0x8))
    geofoffset = fl.tell()
    geneeoflength += geofoffset
    files,null2,plus_value,geneeoflength = struct.unpack('<4I',fl.read(0x10))

    tmpoffset = fl.tell()
    tmp = number
    tmp *= 4
    tmpoffset += tmp

    fl.seek(tmpoffset)
    nameoffset, = struct.unpack('<I',fl.read(0x4))
    nameoffset += plus_value
    nameoffset += geofoffset

    fl.seek(nameoffset)
    fullname,end = test_scr(fl)
    return fullname
    
srcfiles = glob.iglob('pack.idx')

for src in srcfiles:
    dirname = os.path.dirname(src)
    filename = os.path.basename(src)
    basename,extname = os.path.splitext(filename)
    filesize = os.path.getsize(src)
    
    fl = open(src,'rb')

    const = 0x10

    fl.seek(0)

    while fl.tell() < filesize:
        offset = fl.tell()
        idstring = fl.read(8)
        start = fl.tell()
        size, = struct.unpack('<Q',fl.read(0x8))

        if idstring == b'ENDILTLE':
            idoffsetvalue = offset 
            fl.seek(offset+const+size)
            offset = fl.tell()
            idstring = fl.read(8)
            start = fl.tell()
            size, = struct.unpack('<Q',fl.read(0x8))

        '''
        if idstring == b'PACKTOC ':
            fl.seek(start)
            #print(idstring)
            handlePackA(fl,filename)
            #break
        '''

        if idstring == b'PACKFSLS':
            fl.seek(start)
            print(idstring)
            handlePackC(fl,filename,idoffsetvalue)
            break

        fl.seek(offset+const+size)

        
                
    fl.close()
