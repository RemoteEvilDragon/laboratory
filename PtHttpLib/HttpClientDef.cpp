#include "HttpClientDef.h"

boost::asio::io_service g_io_service;

void handle_response(const ResponseInfo& r)
{
    if (r.timeout)
    {
        std::cout << "timeout" << std::endl;
    }
    else if (!r.error_msg.empty())
    {
        std::cout << r.error_msg.c_str() << std::endl;
    }
    else if (-1 == r.status_code)
    {
        std::cout << "unknown error" << std::endl;
    }
    else if (200 != r.status_code)
    {
        std::cout << "http error: " << r.status_code << ", " << r.status_msg << std::endl;
    }
    else
    {
        std::cout << "response size=" << r.content.size()
        << ", content:\r\n" << r.content.c_str() << std::endl;
    }
}

void cb_async_http(boost::shared_ptr<CAsyncHttpClient>& pClient,
                   const ResponseInfo& r)
{
    handle_response(r);
}


void thread_async()
{
        RequestInfo req;
    
        req.set_url("http://www.baidu.com/");
        req.set_method(METHOD_GET);
        
        boost::shared_ptr<CAsyncHttpClient> pClient = boost::make_shared<CAsyncHttpClient>(boost::ref(g_io_service), 5);
        
        pClient->make_request(req, boost::bind(cb_async_http, pClient, _1));
        
        boost::this_thread::sleep(boost::posix_time::seconds(1));
}


void test_async()
{
    boost::thread t(thread_async);
    {
        boost::asio::io_service::work work(g_io_service);
        g_io_service.run();
    }
}


// int main()
// {
//     test_async();
//     return 0;
// }



