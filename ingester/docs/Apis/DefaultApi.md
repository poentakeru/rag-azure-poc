# DefaultApi

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**uploadFileUploadPost**](DefaultApi.md#uploadFileUploadPost) | **POST** /upload | Upload File |
| [**searchSearchGet**](DefaultApi.md#searchSearchGet) | **GET** /search | Search |

<a name="uploadFileUploadPost"></a>
## **uploadFileUploadPost**
> UploadResponse uploadFileUploadPost(file)

Upload File

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **file** | **file**| File to upload | [required] |

### Return type

[**UploadResponse**](../Models/UploadResponse.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: multipart/form-data
- **Accept**: application/json

<a name="searchSearchGet"></a>
## **searchSearchGet**
> SearchResponse searchSearchGet(query, top_k=3)

Search

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **query** | **String**| Query string | [required] |
| **top_k** | **Integer**| Number of results | [optional][default to 3] |

### Return type

[**SearchResponse**](../Models/SearchResponse.md)

### Authorization

No authorization required

### HTTP request headers

- **Accept**: application/json
