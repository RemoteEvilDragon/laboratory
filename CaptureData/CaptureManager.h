#ifndef _CaptureManager_h
#define _CaptureManager_h
#import <UIKit/UIKit.h>

//Camera
#import <UIKit/UIKit.h>
#import <AVFoundation/AVFoundation.h>
#import <CoreGraphics/CoreGraphics.h>
#import <CoreVideo/CoreVideo.h>
#import <CoreMedia/CoreMedia.h>
#include <mutex>
class CaptureDataController;

@interface CaptureManager : NSObject  <AVCaptureVideoDataOutputSampleBufferDelegate> {

    AVCaptureSession *_captureSession;
    BOOL                   m_firstFrame;
    size_t                 m_cameraWidth;
    size_t                 m_cameraHeight;
    size_t                 m_FormatSize;
    BOOL m_bIsEnd;
//    typedef void (T::*HandlerPtr)(void* param);
//    HandlerPtr handler;
@public
    int g_bStartCamera ;
    size_t  g_cameraWidth;
    size_t  g_cameraHeight;
    uint8_t * g_CaptureBuffer ;
    CaptureDataController* m_captureDataController;
	std::mutex m_bufferLock;
}


+(id)sharedManager;
- (void)InitCameraWithTimeValue: (int) ctTimeValue TimeScale:(int) ctTimeScale;
- (AVCaptureDevice *)getFrontCamera;
- (void) closeCapture;

- (BOOL) getStatus;

@end

#endif
