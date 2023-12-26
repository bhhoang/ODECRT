package vn.edu.usth.ocrapp

import android.content.ContentValues
import android.net.Uri
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.provider.MediaStore
import android.view.View
import androidx.activity.viewModels
import androidx.activity.result.contract.ActivityResultContracts
import androidx.coordinatorlayout.widget.CoordinatorLayout
import com.google.android.material.button.MaterialButton
import com.google.android.material.button.MaterialButtonToggleGroup
import com.google.android.material.floatingactionbutton.FloatingActionButton
import com.google.android.material.snackbar.Snackbar

import vn.edu.usth.ocrapp.databinding.ActivityMainBinding

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
            viewModel.setImageUri(uri)
            uploadButton.visibility = View.VISIBLE
            Snackbar.make(coordinatorLayout, "Image selected", Snackbar.LENGTH_LONG)
                .setAction("Undo") {
                    toggleGroup.clearChecked()
                    viewModel.resetImageUri()
                    uploadButton.visibility = View.INVISIBLE
                }
                .show()
        }
    private val takePictureLauncher =
        registerForActivityResult(ActivityResultContracts.TakePicture()) { success ->
            if (!success) {
                return@registerForActivityResult
            }
            viewModel.setImageUri(cameraResultUri)
            uploadButton.visibility = View.VISIBLE
            Snackbar.make(coordinatorLayout, "Image selected", Snackbar.LENGTH_LONG)
                .setAction("Undo") {
                    toggleGroup.clearChecked()
                    viewModel.resetImageUri()
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
            ) ?: return@setOnClickListener
            takePictureLauncher.launch(cameraResultUri)
        }

        uploadButton.setOnClickListener() {
            // Upload image
        }
    }
}