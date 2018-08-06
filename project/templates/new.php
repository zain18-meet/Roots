<form action="<? echo $_SERVER['PHP_SELF'] ?>" method="post" name="main" enctype="multipart/form-data" >
<input name="image" type="file" />//file upload
</form>


<?php
if (!empty($_FILES['image']['name'])) {
    $errors      = array();

    $allowed_ext = array(
        'png',
        'bmp',
        'jpg',
        'jpeg',
        'JPG',
        'PNG',
        'JPEG'
    ); //do neccessary validation

    $file_name   = $_FILES['image']['name'];
    $array       = explode('.', $file_name);
    $file_ext    = end($array);
    $file_size   = $_FILES['image']['size'];
    $file_tmp    = $_FILES['image']['tmp_name'];

    if (!(in_array($file_ext, $allowed_ext) == false) || empty($_FILES['image']['name'])) {

        if ($file_size < 40097152 || empty($_FILES['image']['name'])) {
            if (empty($errors)) {
                $dir    = "./images";
                $userid = isset($_POST['userid']) ? $_POST['userid'] : "";
                $dir1   = $dir . "/" . $userid;
                if (!is_dir($dir1)) {
                    mkdir($dir1);
                }

                move_uploaded_file($file_tmp, $dir1 . "/" . $file_name);

            } else {

                foreach ($errors as $error) {
                    $flag = 0;
                    echo "<script language=javascript> alert(\"File upload error

    \");</script>";
                }
            }
        } else {
            $flag = 0;
            echo "<script language=javascript> alert(\"File Size Limit 20MB\");</script>";