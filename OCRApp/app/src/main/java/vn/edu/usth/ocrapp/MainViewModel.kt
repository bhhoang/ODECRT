package vn.edu.usth.ocrapp

import android.net.Uri
import androidx.activity.result.contract.ActivityResultContracts
import androidx.lifecycle.ViewModel

class MainViewModel: ViewModel() {
    private var _imageUri: Uri = Uri.EMPTY

    val imageUri: Uri get() = _imageUri

    init {

    }

    fun uploadImage() {
        // Upload image to server
    }

    fun setImageUri(uri: Uri) {
        _imageUri = uri
    }
    fun resetImageUri() {
        _imageUri = Uri.EMPTY
    }

}