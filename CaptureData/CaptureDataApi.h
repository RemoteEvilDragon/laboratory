//
//  CaptureDataApi.h
//  GrapeTangarm
//
//  Created by victor ma on 5/18/15.
//
//

#ifndef __CaptureDataApi__
#define __CaptureDataApi__

#include "cocos2d.h"
using namespace cocos2d;
using namespace std;
#include <stdio.h>

typedef struct captureBuffer
{
    int  bufferId ;
    size_t  g_cameraWidth;
    size_t  g_cameraHeight;
    size_t  g_FormatSize;
    uint8_t *g_CaptureBuffer;
    int pt_device;

}captureBuffer;

class CaptureDataController;

class  CaptureDataApi : public Ref
{
protected:
    CaptureDataApi();
    bool init();
public:
    virtual ~CaptureDataApi();
    static CaptureDataApi* getInstance();
    //captureframeduration = ctTimeValue/ctTimeScale;  min 1/60 max 1/2
    void openCaptureForGetBuffer(int ctTimeValue = 1, int ctTimeScale = 30);
    void closeCapture();
    const char*  callLuaFunction(const char* luaFileName,const char* functionName);
    void captureOutputSampleBuffer(size_t  g_cameraWidth,
                                   size_t  g_cameraHeight,
                                   size_t  m_FormatSize,
                                   uint8_t * g_CaptureBuffer,
                                   int pt_device);
    void getBufferInfo(captureBuffer * pBuff);
    bool isHaveBuffer;
    static void sleepIniOS(double t);
private:
	std::mutex m_lock;
    CaptureDataController * m_captureDataController;
    captureBuffer* m_captureBuffer;
};
#endif /* defined(__GrapeTangarm__CaptureDataApi__) */
