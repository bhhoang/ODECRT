package vn.edu.usth.ocrapp

import android.net.Uri
import android.util.Log
import androidx.lifecycle.ViewModel
import java.io.File

import io.ktor.client.*
import io.ktor.client.engine.cio.*
import io.ktor.client.plugins.DefaultRequest
import io.ktor.client.request.*
import io.ktor.client.request.forms.*
import io.ktor.client.statement.*
import io.ktor.http.*
import io.ktor.util.InternalAPI

class MainViewModel: ViewModel() {
    private val url: String = "http://192.168.110.234:5000/upload"
    var file: File? = null

    @OptIn(InternalAPI::class)
    suspend fun uploadImage(): String {
        val httpClient = HttpClient(CIO) {
            engine {
                requestTimeout = 0
            }
            install(DefaultRequest) {
                header(HttpHeaders.ContentType, ContentType.MultiPart.FormData)
            }
        }
        // input image stream from content resolver
        httpClient.use { client ->
            val response: HttpResponse = client.post(url) {
                Log.d("FILE", file.toString())
                body = MultiPartFormDataContent(formData {
                    append("file", file!!.readBytes(), Headers.build {
                        append(HttpHeaders.ContentDisposition, "filename=${file!!.name}")
                    })
                })
            }
            return response.bodyAsText()
        }
    }
}