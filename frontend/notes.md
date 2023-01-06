signupdan sonra profil fotosu dogum tarihi sectir takip etmesi icin onerilerde bulun

signup enter de problem var
tweet btn bos tweet disabled button



<img :src="previewImage" class="uploading-image"/>
<input type="file" @change=uploadImage>


<img :src="data" class="uploading-image"/>
<button @click="testbtn">test</button>
data yerine base 64 gelince fotoyu basiyor

return {
    data: base64 image b'lmem ne
    previewImage: null,
    testImage: null,
}

uploadImage(e){
    const image = e.target.files[0];
    const reader = new FileReader();
    reader.readAsDataURL(image);
    reader.onload = e =>{
        this.previewImage = e.target.result;
        console.log(this.previewImage);
    }
},