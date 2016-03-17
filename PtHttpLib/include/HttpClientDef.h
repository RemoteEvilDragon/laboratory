#define HAS_HTTP_CLIENT_LOG
#include <boost/thread.hpp>
#include <boost/make_shared.hpp>
#include "asynchttpclient.h"

void test_async();
void thread_async();
void cb_async_http(boost::shared_ptr<CAsyncHttpClient>& pClient,const ResponseInfo& r);
void handle_response(const ResponseInfo& r);