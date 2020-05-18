# gcs_pypi

![Python package](https://github.com/jackton1/gcs_pypi/workflows/Python%20package/badge.svg)

gcs-pypi is a CLI for creating a Python Package Repository in an GCS bucket.


## Getting started

### Installation

Install gcs-pypi using pip:

```bash
pip install gcs-pypi
```


## Usage

### GCS Bucket

- Create a new bucket

#### IAM (Role & Service Account)

Setup service account with the following permissions

```text
storage.buckets.get
storage.buckets.getIamPolicy
storage.buckets.update
storage.objects.create
storage.objects.delete
storage.objects.get
storage.objects.getIamPolicy
storage.objects.list
storage.objects.setIamPolicy
```

Recommended that you create a custom Role which can be inherited by the service account

Example

- Create Role "PYPI"

- Assign Permissions

```text
storage.buckets.get
storage.buckets.getIamPolicy
storage.buckets.update
storage.objects.create
storage.objects.delete
storage.objects.get
storage.objects.getIamPolicy
storage.objects.list
storage.objects.setIamPolicy
```

- Create a Service Account e.g pypi

- Select the "PYPI" Role created above

- Add a condition to limit access to only that GCS bucket

```yaml
resource.name == "mybucket"
```

Visit [Cloud IAM Conditions](https://cloud.google.com/iam/docs/conditions-overview?_gac=1.79817061.1587676512.CjwKCAjw-YT1BRAFEiwAd2WRtsely2bRUq6KF3rxDzHVoCLbdZoy-AqW0raFx96lJeQ6O2Ie8q6IMhoCrskQAvD_BwE&_ga=2.40552928.-350153010.1574411744)  for more information


### Distributing packages

You can now use ``gcspypi`` to create Python packages and upload them to your GCS bucket. 
To hide packages from the public, you can use the ``--private`` option to prevent the packages from 
being accessible directly via the GCS bucket (they will only be accessible via your Domain or 
alternatively you can specify a secret subdirectory using the ``--secret`` option:

```bash
cd /path/to/your-project/
gcspypi --bucket mybucket [--private] [--secret SECRET]
```

### Cache Header

Set cache-control header for index.html

```bash
$ gsutil setmeta -h "cache-control:public, must-revalidate, proxy-revalidate, max-age=0" gs://[BUCKET]/index.html
```


### Installing packages

Install your packages using ``pip`` by pointing the ``--extra-index-url`` to your Custom domain (optionally followed by a secret subdirectory):

```bash
pip install your-project --extra-index-url https://pypi.example.com/SECRET/
```

Alternatively, you can configure the index URL in ``~/.pip/pip.conf``:

```
[global]
extra-index-url = https://pypi.example.com/SECRET/
```


#### Credits
- [s3pypi](https://github.com/novemberfiveco/s3pypi)
