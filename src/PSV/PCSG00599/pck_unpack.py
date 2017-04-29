import io,os,struct,glob,codecs,math

srcfiles = glob.iglob('*.pck')

for src in srcfiles:
    fl = open(src,'rb')
    dirname = os.path.dirname(src)
    filename = os.path.basename(src)
    
    idstring1 = fl.read(8) # Filename
    pack_start, = struct.unpack('<I',fl.read(4))
    #pack_start += 0x2
    if (pack_start % 4) != 0:
        pack_start //= 0x4
        pack_start += 1
        pack_start *= 0x4

    breakpoint = fl.tell()
    const = breakpoint
    fl.seek(pack_start)
    #print(pack_start)
    idstring2 = fl.read(8) # Pack    
    #print(idstring2)

    table_size, = struct.unpack('<I',fl.read(4))
    files, = struct.unpack('<I',fl.read(4))
   
    for i in range(files):
        offset, = struct.unpack('<I',fl.read(4))
        size, = struct.unpack('<I',fl.read(4))
        breakpoint2 = fl.tell()
        fl.seek(breakpoint)
        name_offset, = struct.unpack('<I',fl.read(4))
        name_offset += const
        breakpoint = fl.tell()
        fl.seek(name_offset)
        
        start = fl.tell()
        test, = struct.unpack('B',fl.read(1))
        while test != 0:
            test, = struct.unpack('B',fl.read(1))
        
        end = fl.tell()
        fl.seek(start)
        name = fl.read(end-start).decode('cp932').rstrip('\x00')
        fl.seek(offset)

        dirname2 = os.path.dirname(name)
        name2 = os.path.basename(name)
        #print(dirname2)

        if os.path.isdir(filename+'_unpacked\\'+dirname2) == False:
            os.makedirs(filename+'_unpacked\\'+dirname2)
            
        old = open(filename+'_unpacked\\'+name,'wb')
        print(filename + ' >> ' + name)
        old.write(fl.read(size))
        fl.seek(breakpoint2)
        old.close()
    
    fl.close()
    
