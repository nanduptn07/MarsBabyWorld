class landing():
    def landingPrice(self,lprice):
        code = "SFLAMINGOE"
        word = ""
        lp = str(lprice)
        for i in range(0,len(lp)):
            print("i",i)
            word =  word + code[int(lp[i])] 
        return print(word)

obj = landing()
obj.landingPrice(115)