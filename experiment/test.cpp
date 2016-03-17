#include <iostream>
#include <curl/curl.h>
#include <thread>

using namespace std;

//multi thread output test here.
static int HttpPost()
{
  CURL *curl;
  CURLcode res;

  /* In windows, this will init the winsock stuff */ 
  curl_global_init(CURL_GLOBAL_ALL);

  /* get a curl handle */ 
  curl = curl_easy_init();

  if(curl) 
  {
    /* First set the URL that is about to receive our POST. This URL can
       just as well be a https:// URL if that is what should receive the
       data. */ 
    curl_easy_setopt(curl, CURLOPT_URL, "http://27.126.181.90:10000");
    /* Now specify the POST data */ 
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, "name=athen&project=curl");
 
    /* Perform the request, res will get the return code */ 
    res = curl_easy_perform(curl);
    /* Check for errors */ 
    if(res != CURLE_OK)
      cerr<< "curl_easy_perform() failed: "<<curl_easy_strerror(res)<< endl;
 
    /* always cleanup */ 
    curl_easy_cleanup(curl);
  }

  curl_global_cleanup();
  return 0;
}

//An indepedent thread is ok,but standard output may not be displayed.
int main(void) 
{
	char parameters[] = "name=athenking";

	std::thread t(HttpPost);
	t.detach();

  	return 1;
}
