import Oram
import random

def TestBasic() :
    oramsize = 1 << 4 - 1
    oram = Oram.Oram(oramsize, 4, 100)
    for key in range(0, oramsize) :
        oram.write(key, str(key))
    for key in range(0, oramsize) :
        try :
            getvalue = oram.read(key).decode("utf-8")
            assert (getvalue == str(key))
        except :
            print( "[TestBasic] key=%d. expecting %s but got %s" % (key, str(key), getvalue) )
            print( "TestBasic failed." )

        print(oram._stash.getSize())
    print( "TestBasic Passed." )

def TestRepeatRW() :
    oramsize = 1 << 4 - 1
    oram = Oram.Oram(oramsize, 4, 100)
    db = {}
    for key in range(0, oramsize) :
        oram.write(key, str(key))
    for key in range(0, oramsize) :
        try :
            getvalue = oram.read(key).decode("utf-8")
            assert (getvalue == str(key))
            oram.write(key, 'v')
        except :
            print( "[TestRepeatRW] key=%d. expecting %s but got %s" % (key, str(key), getvalue) )
            return
    

def TestGeneral() :
    oramsize = 25
    oram = Oram.Oram(oramsize, 4, 100)
    check  = {}
    N = 10
    numTests = 10
    
    lastStashSize = 0
    currentStashSize = 0
	
    for key in range(1, N) :                 # writes a "random" string to each key from 0 to N
        data = "v" + str(random.randint(1,1000))
        oram.write(key, data)
        check[key] = data	
		
        currentStashSize = oram._stash.getSize()
        print ("ORAM Stash Size: ", currentStashSize)		
        if 	currentStashSize - lastStashSize > 1:
            print("Stash increases by more than 1")			
            exit(0)
        lastStashSize = currentStashSize			
        
    for i in range(0, numTests):        # does a random operation
        operation = random.random()
        key = random.randint(1, N-1)
        if (operation < .2):
            data = "x" + str(random.randint(1,1000))
            oram.write(key, data)
            check[key] = data

        elif (operation <.6):
            try:
                getValue = oram.read(key).decode("utf-8")
                assert (getValue == check[key])
            except:
                print( "[TestGeneral] key=%d. expecting %s but got %s" % (key, check[key], getValue) )
                return

        else:
            if (check[key] != ""):
                oram.delete(key)
                check[key] = ""
        
        currentStashSize = oram._stash.getSize()
        print ("ORAM Stash Size: ", currentStashSize)		
        if 	currentStashSize - lastStashSize > 1:
            print("Stash increases by more than 1")			
            exit(0)	
        lastStashSize = currentStashSize
        
    print ("TestGeneral Passed")

#TestBasic()
# TestRepeatRW()
TestGeneral()
