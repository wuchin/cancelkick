from linepy import *
from thrift.unverting import *
from thrift.TMultiplexedProcessor import *
from thrift.TSerialization import *
from thrift.TRecursive import *
from thrift import transport, protocol, server
import time
kr = LINE()
kr.log("Auth Token : " + str(kr.authToken))
poll = OEPoll(kr)
Owner = ["u9cc2323f5b84f9df880c33aa9f9e3ae1"]
while True:
    try:
        ops = poll.singleTrace(count=50)
        if ops != None:
            for op in ops:
                if (op.type == 13 or op.type == 19):
                    kr.acceptGroupInvitation(op.param1)
                    kr.sendMessage(op.param1,'Cancelling..')
                    s = time.time()
                    kr.sendMessage(op.param1,'Speed!')
                    e = time.time() - s
                    kr.sendMessage(op.param1,'{:.14f}'.format(e))
                    g = kr.getCompactGroup(op.param1)
                    mids = [i.mid for i in g.invitee]
                    for mid in mids:
                        try:
                            kr.cancelGroupInvitation(op.param1,[mid])
                        except Exception as e:
                            pass
                    kr.sendMessage(op.param1,'Done!\nCanceling..!!!')
                    print("sukses cancel")
                    g = kr.getCompactGroup(op.param1)
                    mids = [i.mid for i in g.members]
                    for mid in mids:
                        try:
                            kr.kickoutFromGroup(op.param1,[mid])
                        except Exception as e:
                            pass
                    print("sukses ratain")
                    Owner = ["u9cc2323f5b84f9df880c33aa9f9e3ae1"]
                    kr.getCompactGroup(op.param1)
                    for GS in Owner:
                        try:
                            kr.findAndAddContactsByMid(GS)
                            kr.inviteIntoGroup(to,[GS])
                        except:
                            pass
                    print("sukses invite owner")
                    kr.leaveGroup(op.param1)
                    print("done, left")
                poll.setRevision(op.revision)
    except Exception as e:
        kr.log("[SINGLE_TRACE] ERROR : " + str(e))
