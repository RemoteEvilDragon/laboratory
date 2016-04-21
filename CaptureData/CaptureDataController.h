#ifndef __CaptureDataController__
#define __CaptureDataController__

using namespace std;
#include <stdio.h>
#include <iostream>

class  CaptureDataController : public Ref
{
public:
    CaptureDataController();
    virtual ~CaptureDataController();
    bool init() { return true; };
    void startGetCaptureData(int ctTimeValue, int ctTimeScale);
    void endGetCaptureData();
    std::string getIOSVersion();
    const char * getDeviceId();
    const char* getUUIDStr();
    std::string  getFileFullPath(const char* fileName);
    const char*  callLuaFunction(const char* luaFileName,const char* functionName);
    void captureOutputSampleBuffer(size_t  g_cameraWidth,
                                   size_t  g_cameraHeight,
                                   size_t   m_FormatSize,
                                   uint8_t * g_CaptureBuffer,
                                   int pt_device
                                   );
    CREATE_FUNC(CaptureDataController);
    static void sleepIniOS(double t);
    
    bool getStatusCamera();
    float getSystemVersion();
    string getAppVersion();
    
    void gotoAppStore();
};
#endif /* defined(__GrapeTangarm__CaptureDataController__) */
