import uvicorn 
from svgkeyer import svg_display 
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import FileResponse
app = FastAPI()
import threading, queue

def showforever(q: queue):
    s = svg_display()
    while True:
        try:
            work = q.get()
        except:
            print("Exception!!!")
            continue

        s.set_chroma(work['chromakey'])
        s.show(work['fname'])

class showdata(BaseModel):
    fname: str
    chromakey: tuple
    subs: list

@app.get("/")
async def root():
    return {
            "message":  "Post data is required",
    }

@app.post("/")
async def bugger(d: showdata):
    fname = d.fname
    chromakey=d.chromakey
    subs = d.subs

    print("subs: ",subs)

    # Do template substitution
    f = open(fname,'r')
    data = f.read()
    f.close()
    for item in subs:
        print("Replacing: ",item[0],item[1])
        data=data.replace(item[0],item[1])

    with open("tmp.svg",'w') as f:
        f.write(data)
    q.put({"fname": "tmp.svg", "chromakey": chromakey})


if __name__ == "__main__":
    q = queue.Queue()
    displaythread = threading.Thread(target=showforever, args=(q,), daemon=True)
    displaythread.start()
    uvicorn.run(app,host="0.0.0.0", port=8001)

