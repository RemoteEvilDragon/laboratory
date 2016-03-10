//
//  CaptureDataApi.cpp
//  GrapeTangarm
//
//  Created by victor ma on 5/18/15.
//
//

#include "CaptureDataApi.h"
#include "CaptureDataController.h" 
static CaptureDataApi* _instance = nullptr;

CaptureDataApi* CaptureDataApi::getInstance()
{
    if (_instance == nullptr)
    {
        _instance = new (std::nothrow) CaptureDataApi();
        if (!_instance->init()) {
            delete _instance;
            _instance = nullptr;
        }
    }
    return _instance;
}


CaptureDataApi::CaptureDataApi()
{
    isHaveBuffer = false;
    m_captureDataController = nullptr;
    m_captureBuffer = nullptr;
    m_captureBuffer = new captureBuffer();
    m_captureBuffer->g_CaptureBuffer = nullptr;
    m_captureBuffer->g_cameraWidth = 0;
    m_captureBuffer->bufferId = 0;
    m_captureBuffer->g_cameraHeight = 0;
}
CaptureDataApi::~CaptureDataApi()
{
    if (m_captureBuffer) {
        if (m_captureBuffer->g_CaptureBuffer) {
            free(m_captureBuffer->g_CaptureBuffer);
        }
        delete m_captureBuffer;
    }
    CC_SAFE_DELETE(m_captureDataController);
    m_captureDataController = nullptr;
}
bool CaptureDataApi::init()
{
#if (CC_TARGET_PLATFORM == CC_PLATFORM_IOS)
    if(m_captureDataController)
        CC_SAFE_DELETE(m_captureDataController);
    
    m_captureDataController = new CaptureDataController();
#endif
    return true;
}
void CaptureDataApi::openCaptureForGetBuffer(int ctTimeValue, int ctTimeScale)
{
#if (CC_TARGET_PLATFORM == CC_PLATFORM_IOS)
    if (m_captureDataController) {
        m_captureDataController->startGetCaptureData(ctTimeValue,ctTimeScale);
    }
#endif
}
void CaptureDataApi::closeCapture()
{
#if (CC_TARGET_PLATFORM == CC_PLATFORM_IOS)
    if (m_captureDataController) {
        m_captureDataController->endGetCaptureData();
    }
#endif
}
void CaptureDataApi::sleepIniOS(double t)
{
#if (CC_TARGET_PLATFORM == CC_PLATFORM_IOS)
	CaptureDataController::sleepIniOS(t);
#endif
}

void CaptureDataApi::getBufferInfo(captureBuffer * pBuff)
{
	m_lock.lock();
	if (m_captureBuffer && m_captureBuffer->g_CaptureBuffer) {
		if (pBuff->g_cameraWidth != m_captureBuffer->g_cameraWidth || pBuff->g_cameraHeight != m_captureBuffer->g_cameraHeight || pBuff->g_FormatSize != m_captureBuffer->g_FormatSize) {
			if (pBuff->g_CaptureBuffer) {
				free(pBuff->g_CaptureBuffer);
			}
			pBuff->g_CaptureBuffer = (uint8_t *)calloc(m_captureBuffer->g_cameraWidth * m_captureBuffer->g_cameraHeight * m_captureBuffer->g_FormatSize, 1);
		}
		pBuff->g_cameraWidth = m_captureBuffer->g_cameraWidth;
		pBuff->g_cameraHeight = m_captureBuffer->g_cameraHeight;
		pBuff->g_FormatSize = m_captureBuffer->g_FormatSize;
		if (pBuff->g_CaptureBuffer) {
			memcpy(pBuff->g_CaptureBuffer, m_captureBuffer->g_CaptureBuffer, m_captureBuffer->g_cameraWidth * m_captureBuffer->g_cameraHeight * m_captureBuffer->g_FormatSize);
		}
        pBuff->pt_device=m_captureBuffer->pt_device;
	}
	m_lock.unlock();
}

void CaptureDataApi::captureOutputSampleBuffer(size_t  g_cameraWidth,
                                               size_t  g_cameraHeight,
                                               size_t  m_FormatSize,
                                               uint8_t * g_CaptureBuffer,
                                               int pt_device)
{
    
	m_lock.lock();
    if (!isHaveBuffer) {
        if (m_captureBuffer->g_CaptureBuffer)
            free(m_captureBuffer->g_CaptureBuffer);
        m_captureBuffer->g_CaptureBuffer = (uint8_t *)calloc(g_cameraWidth * g_cameraHeight * m_FormatSize, 1);
        isHaveBuffer = true;
    }

    m_captureBuffer->g_cameraWidth = g_cameraWidth;
    m_captureBuffer->g_cameraHeight = g_cameraHeight;
    m_captureBuffer->g_FormatSize = m_FormatSize;
    m_captureBuffer->pt_device = pt_device;
    memcpy(m_captureBuffer->g_CaptureBuffer, g_CaptureBuffer, g_cameraWidth * g_cameraHeight * m_FormatSize);
    m_captureBuffer->bufferId++;
	m_lock.unlock();
}

const char*  CaptureDataApi::callLuaFunction(const char* luaFileName,const char* functionName){
#if (CC_TARGET_PLATFORM == CC_PLATFORM_IOS)
    const char* iResult =m_captureDataController->callLuaFunction(luaFileName, functionName);
	return iResult;
#else
	return nullptr;
#endif
}