
def codynaqdouble(googlePostCommitData, postFinishedData,changeRequestData):
    global codynaq_dispatchQ
    index=0
    size=changeRequestData.Change_Request.count()
    print("Size : ",size)
    dispatchQueue=pd.DataFrame()
    while True :
        if(index<=size):
            if (len(dispatchQueue)==0):
                dispatchQueue=changeRequestData[index:index+60]
                newDispatchQueue = dispatchQueue.copy(deep = True)
                newDispatchQueue['Priority'] = 0.5
                index=index+60
            if (len(dispatchQueue)!=0):
                result_data_frames = codynaqsingle(googlePostCommitData, postFinishedData,dispatchQueue,newDispatchQueue)
                postFinishedData = result_data_frames[0]
                temp_codynaqD = result_data_frames[1].sort_values('Priority', ascending = False)
                codynaq_dispatchQ = codynaq_dispatchQ.append(temp_codynaqD,ignore_index = True)                
                dispatchQueue=pd.DataFrame()
        else:
            break        
    return codynaq_dispatchQ