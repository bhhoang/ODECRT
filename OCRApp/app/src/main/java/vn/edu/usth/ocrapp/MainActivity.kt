package vn.edu.usth.ocrapp

import android.content.ClipData
import android.content.ClipboardManager
import android.content.ContentValues
import android.net.Uri
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.provider.MediaStore
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.widget.TextView
import androidx.activity.viewModels
import androidx.activity.result.contract.ActivityResultContracts
import androidx.coordinatorlayout.widget.CoordinatorLayout
import androidx.lifecycle.viewModelScope
import com.google.android.material.bottomsheet.BottomSheetDialog
import com.google.android.material.button.MaterialButton
import com.google.android.material.button.MaterialButtonToggleGroup
import com.google.android.material.dialog.MaterialAlertDialogBuilder
import com.google.android.material.floatingactionbutton.FloatingActionButton
import com.google.android.material.snackbar.Snackbar
import kotlinx.coroutines.launch

import kotlinx.serialization.json.*

import vn.edu.usth.ocrapp.databinding.ActivityMainBinding
import java.io.File

class MainActivity : AppCompatActivity() {
    private lateinit var binding: ActivityMainBinding
    private val viewModel: MainViewModel by viewModels()

    private lateinit var coordinatorLayout: CoordinatorLayout
    private lateinit var toggleGroup: MaterialButtonToggleGroup
    private lateinit var folderButton: MaterialButton
    private lateinit var uploadButton: FloatingActionButton

    private lateinit var cameraResultUri: Uri
    private val getFileLauncher =
        registerForActivityResult(ActivityResultContracts.GetContent()) { uri ->
            if (uri == null) {
                return@registerForActivityResult
            }

            val inputStream = contentResolver.openInputStream(uri)
            val byteArray = inputStream?.readBytes()
            val file = File.createTempFile("image", ".jpg", cacheDir)
            file.writeBytes(byteArray!!)
            viewModel.file = file

            Log.d("FILE", file.toString())
            uploadButton.visibility = View.VISIBLE
            Snackbar.make(coordinatorLayout, "Image selected", Snackbar.LENGTH_LONG)
                .setAction("Undo") {
                    toggleGroup.clearChecked()
                    viewModel.file = null
                    uploadButton.visibility = View.INVISIBLE
                }
                .show()
            }

    private val takePictureLauncher =
        registerForActivityResult(ActivityResultContracts.TakePicture()) { success ->
            if (!success) {
                return@registerForActivityResult
            }
            val inputStream = contentResolver.openInputStream(cameraResultUri)
            val byteArray = inputStream?.readBytes()
            val file = File.createTempFile("image", ".jpg", cacheDir)
            file.writeBytes(byteArray!!)
            viewModel.file = file

            uploadButton.visibility = View.VISIBLE
            Snackbar.make(coordinatorLayout, "Image selected", Snackbar.LENGTH_LONG)
                .setAction("Undo") {
                    toggleGroup.clearChecked()
                    viewModel.file = null
                    uploadButton.visibility = View.INVISIBLE
                }
                .show()


        }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        coordinatorLayout = binding.coordinatorLayoutMain
        toggleGroup = binding.toggleGroupMain
        folderButton = binding.buttonMainFolder
        val cameraButton = binding.buttonMainCamera
        uploadButton = binding.floatingActionButtonMainUpload
        val progressBar = binding.progressBarMain

        folderButton.setOnClickListener() {
            // Open folder
            getFileLauncher.launch("image/*")
        }

        cameraButton.setOnClickListener() {
            // Open camera
            val timestamp = System.currentTimeMillis()

            val values = ContentValues().apply {
                put(MediaStore.Images.Media.DISPLAY_NAME, "IMG_${timestamp}.jpg")
                put(MediaStore.Images.Media.MIME_TYPE, "image/jpeg")
            }

            cameraResultUri = contentResolver.insert(
                MediaStore.Images.Media.EXTERNAL_CONTENT_URI,
                values
            )!!
            Log.d("URI", cameraResultUri.toString())
            takePictureLauncher.launch(cameraResultUri)
        }

        uploadButton.setOnClickListener() {
            toggleGroup.clearChecked()
            uploadButton.visibility = View.INVISIBLE
            progressBar.visibility = View.VISIBLE

            viewModel.viewModelScope.launch {
                val result = viewModel.uploadImage()
                val resultObj = Json.decodeFromString<ResultData>(result)
                val resultContent = resultObj.result

                MaterialAlertDialogBuilder(this@MainActivity)
                    .setTitle("Result")
                    .setMessage(resultContent)
                    .setNegativeButton("Close") { dialog, _ ->
                        dialog.dismiss()
                    }
                    .setPositiveButton("Copy") { _, _ ->
                        val clipboard = getSystemService(CLIPBOARD_SERVICE) as ClipboardManager
                        val clip = ClipData.newPlainText("result", resultContent)
                        clipboard.setPrimaryClip(clip)
                    }
                    .show()
                viewModel.file = null
                progressBar.visibility = View.INVISIBLE
            }
        }
    }
}