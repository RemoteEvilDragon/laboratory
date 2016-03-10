#include "CaptureDataController.h"
#include "CCLuaEngine.h"
#import  "CaptureData/CaptureManager.h"
#include "CaptureDataApi.h"
#import "sys/sysctl.h"
#import  "KeychainItemWrapper.h"
#import <Security/SecItem.h>

extern "C"
{
#include "lua.h"
#include "lauxlib.h"
#include "lualib.h"
}

CaptureDataController::CaptureDataController()
{
    CaptureManager * manager = [CaptureManager sharedManager];
    manager->m_captureDataController = this;
}
CaptureDataController::~CaptureDataController()
{
    endGetCaptureData();
}
void CaptureDataController::startGetCaptureData(int ctTimeValue, int ctTimeScale)
{
    CaptureManager * manager = [CaptureManager sharedManager];
    [manager InitCameraWithTimeValue:ctTimeValue TimeScale:ctTimeScale];
}
void CaptureDataController::endGetCaptureData()
{
    CaptureManager * manager = [CaptureManager sharedManager];
    [manager closeCapture];
}

string CaptureDataController::getIOSVersion()
{
    size_t size;
    int nR = sysctlbyname("hw.machine", NULL, &size, NULL, 0);
    char *machine = (char *)malloc(size);
    nR = sysctlbyname("hw.machine", machine, &size, NULL, 0);
    NSString *platform = [NSString stringWithCString:machine encoding:NSUTF8StringEncoding];
    free(machine);
    
//    NSLog(@"name: %@", [[UIDevice currentDevice] name]);
//    NSLog(@"systemName: %@", [[UIDevice currentDevice] systemName]);
//    NSLog(@"systemVersion: %@", [[UIDevice currentDevice] systemVersion]);
//    NSLog(@"model: %@", [[UIDevice currentDevice] model]);
    
    const char* systemVersion = [[[UIDevice currentDevice] systemVersion] UTF8String];
    string Str(systemVersion);
    if ([platform isEqualToString:@"iPhone1,1"]) return "iphone_1|" + Str;
    if ([platform isEqualToString:@"iPhone1,2"]) return "iphone_3|"  + Str;
    if ([platform isEqualToString:@"iPhone2,1"]) return "iphone_3gs|" + Str;
    if ([platform isEqualToString:@"iPhone3,1"]) return "iphone_4|" + Str;
    if ([platform isEqualToString:@"iPhone3,2"]) return "iphone_4|" + Str;
    if ([platform isEqualToString:@"iPhone3,3"]) return "iphone_4|" + Str;
    if ([platform isEqualToString:@"iPhone4,1"]) return "iphone_4s|" + Str;
    if ([platform isEqualToString:@"iPhone5,1"]) return "iphone_5|" + Str;
    if ([platform isEqualToString:@"iPhone5,2"]) return "iphone_5|" + Str;
    if ([platform isEqualToString:@"iPhone5,3"]) return "iphone_5c|" + Str;
    if ([platform isEqualToString:@"iPhone5,4"]) return "iphone_5c|" + Str;
    if ([platform isEqualToString:@"iPhone6,1"]) return "iphone_5s|" + Str;
    if ([platform isEqualToString:@"iPhone6,2"]) return "iphone_5s|" + Str;
    if ([platform isEqualToString:@"iPhone7,1"]) return "iphone_6|" + Str;
    if ([platform isEqualToString:@"iPhone7,2"]) return "iphone_6_plus|" + Str;
    //iPot Touch
    if ([platform isEqualToString:@"iPod1,1"]) return "ipod_touch|" + Str;
    if ([platform isEqualToString:@"iPod2,1"]) return "ipod_touch_2|" + Str;
    if ([platform isEqualToString:@"iPod3,1"]) return "ipod_touch_3|" + Str;
    if ([platform isEqualToString:@"iPod4,1"]) return "ipod_touch_4|" + Str;
    if ([platform isEqualToString:@"iPod5,1"]) return "ipod_touch_5|" + Str;
    //iPad#
    if ([platform isEqualToString:@"iPad1,1"]) return "ipad|" + Str;
    if ([platform isEqualToString:@"iPad2,1"]) return "ipad_2|" + Str;
    if ([platform isEqualToString:@"iPad2,2"]) return "ipad_2|" + Str;
    if ([platform isEqualToString:@"iPad2,3"]) return "ipad_2|" + Str;
    if ([platform isEqualToString:@"iPad2,4"]) return "ipad_2|" + Str;
    if ([platform isEqualToString:@"iPad2,5"]) return "ipad_mini_1|" + Str;
    if ([platform isEqualToString:@"iPad2,6"]) return "ipad_mini_1|" + Str;
    if ([platform isEqualToString:@"iPad2,7"]) return "ipad_mini_1|" + Str;
    if ([platform isEqualToString:@"iPad3,1"]) return "ipad_3|" + Str;
    if ([platform isEqualToString:@"iPad3,2"]) return "ipad_3|" + Str;
    if ([platform isEqualToString:@"iPad3,3"]) return "ipad_3" + Str;
    if ([platform isEqualToString:@"iPad3,4"]) return "ipad_4|" + Str;
    if ([platform isEqualToString:@"iPad3,5"]) return "ipad_4|" + Str;
    if ([platform isEqualToString:@"iPad3,6"]) return "ipad_4|" + Str;
    if ([platform isEqualToString:@"iPad4,1"]) return "ipad_air|" + Str;
    if ([platform isEqualToString:@"iPad4,2"]) return "ipad_air|" + Str;
    if ([platform isEqualToString:@"iPad4,3"]) return "ipad_air|" + Str;
    if ([platform isEqualToString:@"iPad4,4"]) return "ipad_mini_2|" + Str;
    if ([platform isEqualToString:@"iPad4,5"]) return "ipad_mini_2|" + Str;
    if ([platform isEqualToString:@"iPad4,6"]) return "ipad_mini_2|" + Str;
    if ([platform isEqualToString:@"iPad4,7"]) return "ipad_mini_3|" + Str;
    if ([platform isEqualToString:@"iPad4,8"]) return "ipad_mini_3|" + Str;
    if ([platform isEqualToString:@"iPad4,9"]) return "ipad_mini_3|" + Str;
    if ([platform isEqualToString:@"iPad5,1"]) return "ipad_mini_4|" + Str;
    if ([platform isEqualToString:@"iPad5,2"]) return "ipad_mini_4|" + Str;
    if ([platform isEqualToString:@"iPad5,3"]) return "ipad_air_2|" + Str;
    if ([platform isEqualToString:@"iPad5,4"]) return "ipad_air_2|" + Str;
    if ([platform isEqualToString:@"iPad6,7"]) return "ipad_pro_1|" + Str;
    if ([platform isEqualToString:@"iPad6,8"]) return "ipad_pro_1|" + Str;
    return "";
}

const char* CaptureDataController::getUUIDStr()
{
    CFUUIDRef pUUID = CFUUIDCreate(nil);
    CFStringRef uuidStr = CFUUIDCreateString(nil, pUUID);
    NSString *result = (NSString*)CFStringCreateCopy(NULL, uuidStr);
    CFRelease(pUUID);
    CFRelease(uuidStr);
    [result autorelease];
    return [result UTF8String];
}

std::string CaptureDataController::getFileFullPath(const char* fileName){
    return FileUtils::getInstance()->fullPathForFilename(fileName);
}

const char*  CaptureDataController::callLuaFunction(const char* luaFileName,const char* functionName){
    lua_State*  ls = LuaEngine::getInstance()->getLuaStack()->getLuaState();
    
    int isOpen =luaL_dofile(ls,getFileFullPath(luaFileName).c_str());
    int status = luaL_loadfile(ls, getFileFullPath(luaFileName).c_str());
    printf("status = %d",status);
    int result = 0;
    if(status == 0)
    {
        result = lua_pcall(ls, 0, LUA_MULTRET, 0);
        cout << " result =="<<result << endl;
    }
    else
    {
        cout << " Could not load the script."<<status << endl;
    }
    if(isOpen!=0){
        CCLOG("Open Lua Error: %i", isOpen);
        return NULL;
    }

    lua_getglobal(ls, functionName);
    lua_pushstring(ls, "Himi");
    lua_pushnumber(ls, 23);
//    lua_pushboolean(ls, true);
    /*
     lua_call
     第一个参数:函数的参数个数
     第二个参数:函数返回值个数
     */
    lua_call(ls, 2, 1);
    
    const char* iResult = lua_tostring(ls, -1);
    
    return iResult;
}
void CaptureDataController::sleepIniOS(double t)
{
    NSLog(@"starttime");
    [NSThread sleepForTimeInterval:t];
    NSLog(@"endtime");
}
void CaptureDataController::captureOutputSampleBuffer(size_t  g_cameraWidth,
                                                      size_t  g_cameraHeight,
                                                      size_t   m_FormatSize,
                                                      uint8_t * g_CaptureBuffer,
                                                      int pt_device
                                                      )
{
    if (CaptureDataApi::getInstance()) {
        CaptureDataApi::getInstance()->captureOutputSampleBuffer(g_cameraWidth, g_cameraHeight,m_FormatSize, g_CaptureBuffer,pt_device);
    }
}


bool CaptureDataController::getStatusCamera()
{
    CaptureManager * manager = [CaptureManager sharedManager];
    return [manager getStatus];
}

float CaptureDataController::getSystemVersion()
{
    float floatString = [[[UIDevice currentDevice] systemVersion] floatValue];
    return floatString;
}

