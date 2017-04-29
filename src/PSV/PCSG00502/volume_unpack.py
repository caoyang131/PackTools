import zlib,os,struct,glob,shutil,codecs

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
    #print(script)
    #end += 1
    return script,end

folder = glob.iglob('volume.dat')
idx = codecs.open('volume.txt','wb','utf16')

for src in folder:
    fl = open(src,'rb')
    dirname = os.path.dirname(src)
    filename = os.path.basename(src)
    if os.path.isdir(filename+'_unpacked\\') == False:
        os.makedirs(filename+'_unpacked\\')
    
    idstring = fl.read(4)

    files1,files2,start = struct.unpack('>3I',fl.read(0xC))
    packsize, = struct.unpack('>I',fl.read(0x4))

    for i in range(files1):
        number1, = struct.unpack('>I',fl.read(0x4))
        number2, = struct.unpack('>I',fl.read(0x4))
        number3, = struct.unpack('>I',fl.read(0x4))
        number4, = struct.unpack('>I',fl.read(0x4))
        number5, = struct.unpack('>I',fl.read(0x4))
        number6, = struct.unpack('>I',fl.read(0x4))

        idx.write(hex(number1)+',')
        idx.write(hex(number2)+',')
        idx.write(hex(number3)+',')
        idx.write(hex(number4)+',')
        idx.write(hex(number5)+',')
        idx.write(hex(number6)+',')

        number2 += start # file_offset
        number5 += start # name_offset
        zsize = number5 - number2 # comp_size
        size = number3

        breakpoint = fl.tell()
        #print(hex(number5))

        fl.seek(number5)
        name,end = test_scr(fl)
        fullname = filename+'_unpacked\\'+name
        print(fullname)
        dirname = os.path.dirname(fullname)

        if os.path.isdir(dirname) == False:
            os.makedirs(dirname)
        new = open(fullname,'wb')
        fl.seek(number2)

        if(size != zsize):
            data = zlib.decompress(fl.read(zsize))
            new.write(data)
        else:
            new.write(fl.read(size))
            
        new.close()
        fl.seek(breakpoint)

        idx.write(name+'\r\n')

    idx.close()
    fl.close()
