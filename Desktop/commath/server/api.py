from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
#from nameko.rpc import rpc
#from nameko.standalone.rpc import ClusterRpcProxy

class eliminate(BaseModel):
    A:list
    b:list
    
    

app = FastAPI() # FlaskApp()

#broker_cfg = {'AMQP_URI': "amqp://guest:guest@rabbitmq"}
origins = [
    "*",
    "http://localhost",
    "http://localhost:80",
    "http://localhost:8000",
    "http://localhost:8000/b2s",
    "http://localhost:8000/elimination",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/b2s/{text}")
def bit2int(text:str):
    s = int(text[0])
    e = int(text[1:9], 2)
    f = [ int(x) for x in text[9:]]
    x = 1 + sum([ int(f[i])*2**(-(i+1)) for i in range(len(f)) ])
    result = (-1)**s * 2**(e-127) * x 
    return result

@app.post("/elimination")
def api(data:eliminate):
    lam = int(data.A[1][0]) / int(data.A[0][0])
    data.A[1] = [ int(x)-lam*int(y) for x,y in zip(data.A[1],data.A[0]) ]
    data.b[1] = int(data.b[1]) - lam*int(data.b[0])
 
    lam = int(data.A[2][0]) / int(data.A[0][0])
    data.A[2] = [ int(x)-lam*int(y) for x,y in zip(data.A[2],data.A[0]) ]
    data.b[2] = int(data.b[2]) - lam*int(data.b[0])
 
    lam = int(data.A[2][1]) / int(data.A[1][1])
    data.A[2] = [ int(x)-lam*int(y) for x,y in zip(data.A[2],data.A[1]) ]
    data.b[2] = int(data.b[2]) - lam*int(data.b[1])

    x2 = int(data.b[2])/int(data.A[2][2])
    x1 = (int(data.b[1]) - int(data.A[1][2])*x2)/int(data.A[1][1])
    x0 = (int(data.b[0]) - int(data.A[0][1])*x1 - int(data.A[0][2])*x2)/int(data.A[0][0])

    result = [x0,x1,x2]
    return result
    
 




# @app.post("/register/")
# def api(student_item: Student):
#     #with ClusterRpcProxy(broker_cfg) as rpc:
#     #    sid =rpc.student.insert(student_item.firstname, student_item.lastname, student_item.email)
#     #    rpc.enroll.insert.call_async(sid, student_item.firstname, student_item.lastname)
#     #    rpc.email.send.call_async(sid, student_item.firstname, student_item.lastname, student_item.email)

#     #print(sid)
#     return {'results': 'registered'}
