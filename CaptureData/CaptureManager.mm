//
//  CaptureManager.m
//  GrapeTangarm
//
//  Created by victor ma on 5/8/15.
//
//


#import "CaptureManager.h"
#include "CaptureDataController.h"
#import "sys/sysctl.h"

@implementation CaptureManager


//@synthesize captureSession = _captureSession;


#pragma mark Singleton Methods



+(id)sharedManager {
    
    static CaptureManager *sharedCaptureManager= nil;
    
    static dispatch_once_t onceToken;
    
    dispatch_once(&onceToken, ^{
        
        sharedCaptureManager = [[self alloc] init];
    
    });
    
    return sharedCaptureManager;
    
}



-(id)init {
    
    if (self = [super init]) {
        
        m_firstFrame = YES;
        m_cameraWidth = 0;
        m_cameraHeight = 0;
        m_FormatSize = 4;
        g_bStartCamera  = 1 ;
        g_cameraWidth   = 0 ;
        g_cameraHeight  = 0 ;
        g_CaptureBuffer = nullptr ;
        m_captureDataController = nullptr ;
        m_bIsEnd = false;
    }
    return self;
    
}



-(void)dealloc {
    [super dealloc];
    [self closeCapture];
    // Should never be called, but justhere for clarity really.
    
}
- (AVCaptureDevice *)getFrontCamera
{
    NSArray *cameras = [AVCaptureDevice devicesWithMediaType:AVMediaTypeVideo];
    for (AVCaptureDevice *device in cameras)
    {
        if (device.position == AVCaptureDevicePositionFront) {
            
            return  device;
        }
    }
    
    return [AVCaptureDevice defaultDeviceWithMediaType:AVMediaTypeVideo];
}
- (NSString*) doDevicePlatform
{
    size_t size;
    int nR = sysctlbyname("hw.machine", NULL, &size, NULL, 0);
    char *machine = (char *)malloc(size);
    nR = sysctlbyname("hw.machine", machine, &size, NULL, 0);
    NSString *platform = [NSString stringWithCString:machine encoding:NSUTF8StringEncoding];
    free(machine);
    if ([platform isEqualToString:@"iPhone1,1"]) return @"iPhone 1";
    if ([platform isEqualToString:@"iPhone1,2"]) return @"iPhone 3";
    if ([platform isEqualToString:@"iPhone2,1"]) return @"iPhone 3GS";
    if ([platform isEqualToString:@"iPhone3,1"]) return @"iPhone 4";
    if ([platform isEqualToString:@"iPhone3,2"]) return @"iPhone 4";
    if ([platform isEqualToString:@"iPhone3,3"]) return @"iPhone 4";
    if ([platform isEqualToString:@"iPhone4,1"]) return @"iPhone 4s";
    if ([platform isEqualToString:@"iPhone5,1"]) return @"iPhone 5";
    if ([platform isEqualToString:@"iPhone5,2"]) return @"iPhone 5";
    if ([platform isEqualToString:@"iPhone5,3"]) return @"iPhone 5C";
    if ([platform isEqualToString:@"iPhone5,4"]) return @"iPhone 5C";
    if ([platform isEqualToString:@"iPhone6,1"]) return @"iPhone 5S";
    if ([platform isEqualToString:@"iPhone6,2"]) return @"iPhone 5S";
    if ([platform isEqualToString:@"iPhone7,1"]) return @"iPhone 6";
    if ([platform isEqualToString:@"iPhone7,2"]) return @"iPhone 6 Plus";
    //iPot Touch
    if ([platform isEqualToString:@"iPod1,1"]) return @"iPod Touch";
    if ([platform isEqualToString:@"iPod2,1"]) return @"iPod Touch 2";
    if ([platform isEqualToString:@"iPod3,1"]) return @"iPod Touch 3";
    if ([platform isEqualToString:@"iPod4,1"]) return @"iPod Touch 4";
    if ([platform isEqualToString:@"iPod5,1"]) return @"iPod Touch 5";
    //iPad
    if ([platform isEqualToString:@"iPad1,1"]) return @"iPad";
    if ([platform isEqualToString:@"iPad2,1"]) return @"iPad 2";
    if ([platform isEqualToString:@"iPad2,2"]) return @"iPad 2";
    if ([platform isEqualToString:@"iPad2,3"]) return @"iPad 2";
    if ([platform isEqualToString:@"iPad2,4"]) return @"iPad 2";
    if ([platform isEqualToString:@"iPad2,5"]) return @"iPad Mini 1";
    if ([platform isEqualToString:@"iPad2,6"]) return @"iPad Mini 1";
    if ([platform isEqualToString:@"iPad2,7"]) return @"iPad Mini 1";
    if ([platform isEqualToString:@"iPad3,1"]) return @"iPad 3";
    if ([platform isEqualToString:@"iPad3,2"]) return @"iPad 3";
    if ([platform isEqualToString:@"iPad3,3"]) return @"iPad 3";
    if ([platform isEqualToString:@"iPad3,4"]) return @"iPad 4";
    if ([platform isEqualToString:@"iPad3,5"]) return @"iPad 4";
    if ([platform isEqualToString:@"iPad3,6"]) return @"iPad 4";
    if ([platform isEqualToString:@"iPad4,1"]) return @"iPad air";
    if ([platform isEqualToString:@"iPad4,2"]) return @"iPad air";
    if ([platform isEqualToString:@"iPad4,3"]) return @"iPad air";
    if ([platform isEqualToString:@"iPad4,4"]) return @"iPad mini 2";
    if ([platform isEqualToString:@"iPad4,5"]) return @"iPad mini 2";
    if ([platform isEqualToString:@"iPad4,6"]) return @"iPad mini 2";
    if ([platform isEqualToString:@"iPad4,7"]) return @"iPad mini 3";
    if ([platform isEqualToString:@"iPad4,8"]) return @"iPad mini 3";
    if ([platform isEqualToString:@"iPad4,9"]) return @"iPad mini 3";
    if ([platform isEqualToString:@"iPad5,3"]) return @"iPad air 2";
    if ([platform isEqualToString:@"iPad5,4"]) return @"iPad air 2";
    NSLog(@"name: %@", [[UIDevice currentDevice] name]);
    NSLog(@"systemName: %@", [[UIDevice currentDevice] systemName]);
    NSLog(@"systemVersion: %@", [[UIDevice currentDevice] systemVersion]);
    NSLog(@"model: %@", [[UIDevice currentDevice] model]);
//    NSLog(@"localizedModel: %@", [self doDevicePlatform]);
    return platform;
}
//PT_DEVICE_IPADMINI         = 0,
//PT_DEVICE_IPAD             = 1,
//PT_DEVICE_COUNT            = 2,
-(int) getPT_DEVICE
{
    size_t size;
    int nR = sysctlbyname("hw.machine", NULL, &size, NULL, 0);
    char *machine = (char *)malloc(size);
    nR = sysctlbyname("hw.machine", machine, &size, NULL, 0);
    NSString *platform = [NSString stringWithCString:machine encoding:NSUTF8StringEncoding];
    free(machine);
    if ([platform isEqualToString:@"iPad1,1"]) return 1;
    if ([platform isEqualToString:@"iPad2,1"]) return 1;
    if ([platform isEqualToString:@"iPad2,2"]) return 1;
    if ([platform isEqualToString:@"iPad2,3"]) return 1;
    if ([platform isEqualToString:@"iPad2,4"]) return 1;
    if ([platform isEqualToString:@"iPad2,5"]) return 0;
    if ([platform isEqualToString:@"iPad2,6"]) return 0;
    if ([platform isEqualToString:@"iPad2,7"]) return 0;
    if ([platform isEqualToString:@"iPad3,1"]) return 1;
    if ([platform isEqualToString:@"iPad3,2"]) return 1;
    if ([platform isEqualToString:@"iPad3,3"]) return 1;
    if ([platform isEqualToString:@"iPad3,4"]) return 1;
    if ([platform isEqualToString:@"iPad3,5"]) return 1;
    if ([platform isEqualToString:@"iPad3,6"]) return 1;
    if ([platform isEqualToString:@"iPad4,1"]) return 1;
    if ([platform isEqualToString:@"iPad4,2"]) return 1;
    if ([platform isEqualToString:@"iPad4,3"]) return 1;
    if ([platform isEqualToString:@"iPad4,4"]) return 0;
    if ([platform isEqualToString:@"iPad4,5"]) return 0;
    if ([platform isEqualToString:@"iPad4,6"]) return 0;
    if ([platform isEqualToString:@"iPad4,7"]) return 0;
    if ([platform isEqualToString:@"iPad4,8"]) return 0;
    if ([platform isEqualToString:@"iPad4,9"]) return 0;
    if ([platform isEqualToString:@"iPad5,3"]) return 1;
    if ([platform isEqualToString:@"iPad5,4"]) return 1;
    return 1;
}
- (void)InitCameraWithTimeValue:  (int) ctTimeValue TimeScale:(int) ctTimeScale {
    NSLog(@"startcapture========");
    m_bIsEnd = false;
    /*And we create a capture session*/
    _captureSession = [[AVCaptureSession alloc] init];
    //setting camera pixel
    _captureSession.sessionPreset =
    AVCaptureSessionPresetLow;
    //AVCaptureSessionPresetMedium;360*..
    //AVCaptureSessionPreset640x480;
    
    
    /*We add input and output*/
    
    
    /*We setup the input*/
    AVCaptureDeviceInput *captureInput = [AVCaptureDeviceInput
                                          deviceInputWithDevice:[self getFrontCamera]
                                          error:nil];
    if (!captureInput) {
        printf("Cannot use camera!\n");
        return;
    }
    
    /*We setupt the output*/
    AVCaptureVideoDataOutput *captureOutput = [[AVCaptureVideoDataOutput alloc] init];
    captureOutput.alwaysDiscardsLateVideoFrames = YES;
    //    captureOutput.minFrameDuration = CMTimeMake(1, 20);// Uncomment it to specify a minimum duration for each video frame
    
    dispatch_queue_t queue = dispatch_queue_create("myQueue", NULL);
    [captureOutput setSampleBufferDelegate:self queue:queue];
    dispatch_release(queue);
    
    //[captureOutput setSampleBufferDelegate:self queue:dispatch_get_main_queue()];
    // Set the video output to store frame in BGRA (It is supposed to be faster)
    NSString* key = (NSString*)kCVPixelBufferPixelFormatTypeKey;
    NSNumber* value = [NSNumber numberWithUnsignedInt:kCVPixelFormatType_32BGRA];
    NSDictionary* videoSettings = [NSDictionary dictionaryWithObject:value forKey:key];
    [captureOutput setVideoSettings:videoSettings];

    [_captureSession addInput:captureInput];
    [_captureSession addOutput:captureOutput];
    [captureOutput release];
    
    [_captureSession beginConfiguration];
    AVCaptureDevice* device  =   [self getFrontCamera];
    if ( YES == [device lockForConfiguration:NULL] )
    {
 /*.................................................................*/
//        [device setActiveVideoMinFrameDuration:CMTimeMake(1,2)];
//        [device setActiveVideoMaxFrameDuration:CMTimeMake(1,2)];
/*.................................................................*/
        
    //add by wangdahu
        NSError *error2;
        //当应用程序不兼容硬件设备时自动改变
        [device lockForConfiguration:&error2];
        if (error2==nil) {
            
            
            
                    if ([device respondsToSelector:@selector(setActiveVideoMinFrameDuration:)]){
                        [device setActiveVideoMinFrameDuration:CMTimeMake(ctTimeValue, ctTimeScale)];
                    }
                    else if([device respondsToSelector:@selector(setActiveVideoMaxFrameDuration:)]){
            
                        [device setActiveVideoMaxFrameDuration:CMTimeMake(ctTimeValue, ctTimeScale)];
                    }
        
//                if (device.activeFormat.videoSupportedFrameRateRanges) {
//                    
//                    [device setActiveVideoMinFrameDuration:CMTimeMake(1, 2)];
//                    [device setActiveVideoMaxFrameDuration:CMTimeMake(1, 2)];
//                    
//                }else{
//                    //
//                }
        }
//        if ([device respondsToSelector:@selector(setActiveVideoMinFrameDuration:)]){
//            [device setActiveVideoMinFrameDuration:CMTimeMake(1,2)];
//        }else{
//            
//            //[device setActiveVideoMaxFrameDuration:CMTimeMake(1, 2)];
//        }
        [device unlockForConfiguration];
    }
    [_captureSession commitConfiguration];
    /*We start the capture*/
    [_captureSession startRunning];
    m_firstFrame = YES;
}
#pragma mark -
#pragma mark AVCaptureSession delegate
- (void)captureOutput:(AVCaptureOutput *)captureOutput
didOutputSampleBuffer:(CMSampleBufferRef)sampleBuffer
       fromConnection:(AVCaptureConnection *)connection
{
    if (g_bStartCamera == 1)
    {
		std::lock_guard < std::mutex > autoLock(m_bufferLock);
        CVImageBufferRef imageBuffer = CMSampleBufferGetImageBuffer(sampleBuffer);
        /*Lock the image buffer*/
        CVPixelBufferLockBaseAddress(imageBuffer,0);
        if (m_firstFrame)
        {
            m_cameraWidth = CVPixelBufferGetWidth(imageBuffer);
            m_cameraHeight = CVPixelBufferGetHeight(imageBuffer);
            
            g_cameraWidth = m_cameraWidth;
            g_cameraHeight = m_cameraHeight;
            
            switch (CVPixelBufferGetPixelFormatType(imageBuffer))
            {
                case kCVPixelFormatType_32BGRA:
                    m_FormatSize = 4;
                    break;
                case kCVPixelFormatType_24RGB:
                    m_FormatSize = 3;
                    break;
                default:
                    m_FormatSize = 4;
                    break;
            }
            g_CaptureBuffer = (uint8_t *)calloc(m_cameraWidth * m_cameraHeight * m_FormatSize, 1);
            m_firstFrame = FALSE;
        }
        /*Get information about the image*/
        uint8_t *baseAddress = (uint8_t *)CVPixelBufferGetBaseAddress(imageBuffer);
        if (g_CaptureBuffer)
        {
            memcpy(g_CaptureBuffer, baseAddress, m_cameraHeight * m_cameraWidth * m_FormatSize);
        }

        /*We unlock the  image buffer*/
        CVPixelBufferUnlockBaseAddress(imageBuffer,0);
        if (m_captureDataController&&!m_bIsEnd) {
           // NSLog(@"captureOutputSampleBuffer========");
            int pt_device = [self getPT_DEVICE];
            m_captureDataController->captureOutputSampleBuffer(g_cameraWidth,
                                                               g_cameraHeight,
                                                               m_FormatSize,
                                                               g_CaptureBuffer,
                                                               pt_device);

        }        
    }
}
- (void) closeCapture
{
    if (!_captureSession || !_captureSession.running)
        return;
    [_captureSession stopRunning];
    [_captureSession release];
    //异步待定
//    dispatch_sync(_captureSessionQueue, ^{
//        NSLog(@"waiting for capture session to end");
//    });
    _captureSession = nil;
	std::lock_guard < std::mutex > autoLock(m_bufferLock);
    if (g_CaptureBuffer) {
        free(g_CaptureBuffer);
    }
    m_firstFrame = YES;
    m_cameraWidth = 0;
    m_cameraHeight = 0;
    m_FormatSize = 4;
    g_bStartCamera  = 1 ;
    g_cameraWidth   = 0 ;
    g_cameraHeight  = 0 ;
    g_CaptureBuffer = nullptr ;
     m_bIsEnd = true;
    NSLog(@"closecapture========");
}

-(BOOL)getStatus
{
    //NSLog(@"systemVersion: %@", [[UIDevice currentDevice] systemVersion]);
    float floatString = [[[UIDevice currentDevice] systemVersion] floatValue];
    if (floatString >= 7.0) {
        NSString *mediaType = AVMediaTypeVideo;
        AVAuthorizationStatus authStatus = [AVCaptureDevice authorizationStatusForMediaType:mediaType];
        if (authStatus == AVAuthorizationStatusDenied) {
            return false;
        }
    }
    
    return true;
}

@end