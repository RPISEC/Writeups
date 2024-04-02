# Blast from the Past

## Foren, 300 points

> The judge for these pictures is a real fan of antiques. Can you age this photo to the specifications?
Set the timestamps on this picture to 1970:01:01 00:00:00.001+00:00 with as much precision as possible for each timestamp. In this example, +00:00 is a timezone adjustment. Any timezone is acceptable as long as the time is equivalent. As an example, this timestamp is acceptable as well: 1969:12:31 19:00:00.001-05:00. For timestamps without a timezone adjustment, put them in GMT time (+00:00). The checker program provides the timestamp needed for each.
>
> Use this [picture](https://artifacts.picoctf.net/c_mimas/75/original.jpg).
>
> **Hint 1:** Exiftool is really good at reading metadata, but you might want to use something else to modify it.

We're given an image file, and we're told we need to resubmit it with specific
timestamp: `1970:01:01 00:00:00.001+00:00`. This time is actually a special
time: the Unix epoch.

Unix time is the amount of seconds passed since 1970, Jan 1 at 00:00:00. So if
we want to set the unix timestamp of the image, we can just set the timestamp
to 0.

We can examine and change the metadata of an image using exiftool. The hint
suggests not using exiftool, but we're going to at least examine the image with
exiftool.

After downloading the image and running `exiftool original.jpg`, exiftool dumps
the metadata of the image. The things we're really interested in are the
timestamps, listed below:

```terminal
...
Date/Time Original              : 2023:11:20 15:46:23
Create Date                     : 2023:11:20 15:46:23
...
Time Stamp                      : 2023:11:20 15:46:21-05:00
...
Create Date                     : 2023:11:20 15:46:23.703
Date/Time Original              : 2023:11:20 15:46:23.703
Modify Date                     : 2023:11:20 15:46:23.703
...
```

Referencing the exif [documentation](https://exiftool.org/#shift), we see that
we can set all dates at once using the -AllDates shortcut. Convenient!

Running `exiftool -AllDates="1970:01:01 00:00:00.001+00:00" original.jpg`, and
then `exiftool original.jpg`, we can see that all dates have been set to the
specified time:

```terminal
Modify Date                     : 1970:01:01 00:00:00
...
Date/Time Original              : 1970:01:01 00:00:00
Create Date                     : 1970:01:01 00:00:00
...
Time Stamp                      : 2023:11:20 15:46:21-05:00
...
Create Date                     : 1970:01:01 00:00:00.703
Date/Time Original              : 1970:01:01 00:00:00.703
Modify Date                     : 1970:01:01 00:00:00.703
...
```

Whoops, we missed one! Time stamp didn't get set. This is because its a non-standard
time stamp element, so the AllDates sorthand didn't cover it.

By using `exiftool original.jpg -s`,  we can find the actual name of the "Time Stamp"
tag. It ends up being simply "TimeStamp", so we can run:
`exiftool -TimeStamp="1970:01:01 00:00:00.001+00:00" original.jpg`.

```terminal
Warning: Not an integer for XMP-apple-fi:TimeStamp
    0 image files updated
    1 image files unchanged
```

Not an integer? TimeStamp is in a different format than the other fields, or
at least exiftool can't automatically convert it for us. Here, we
use our knowledge of Unix Time, and set it to zero instead.

`exiftool -TimeStamp=0 original.jpg`

Now all the date fields are timestamped correctly. We submit the image, and...

```terminal
Checking tag 4/7
Looking at Composite: SubSecCreateDate
Looking for '1970:01:01 00:00:00.001'
Found: 1970:01:01 00:00:00.703
Oops! That tag isn't right. Please try again.
```

We missed the Composite SubSecCreateDate tag! Sub Seconds are stored in a
separate flag, we set the `SubSecCreateDate`, `SubSecDateTimeOriginal`, and
`SubSecModifyDate`. Resubmit...

```terminal
Checking tag 7/7
Timezones do not have to match, as long as it's the equivalent time.
Looking at Samsung: TimeStamp
Looking for '1970:01:01 00:00:00.001+00:00'
Found: 2023:11:20 20:46:21.420+00:00
Oops! That tag isn't right. Please try again.
```

We already set timestamp, but it seems that the time still exists somewhere in
the metadata. It doesn't show up when we run exiftool, so it looks like we'll
have to look for it in the binary.

Doing a quick scan for "Samsung: TimeStamp" or just "TimeStamp" didn't
return anything, so we scan through the binary manually. At the end of the
file, after the image block, we can see that the end of the file has
the ascii text `Image_UTC_Data1700513181420`. Converting the number at
the end gives `Mon Nov 20 2023 20:46:21 GMT+0000`, the time in that the
file checker found! We manually set the bits to `Image_UTC_Data0000000000001`
to set the time to the unix epoch, and resubmit...

```terminal
You did it!
picoCTF{71m3_7r4v311ng_p1c7ur3_ed953b57}
```
