# Stream Cloud Pub/Sub with Cloud Dataflow

Sample(s) showing how to use [Google Cloud Pub/Sub] with [Google Cloud Dataflow].

## Before you begin

1. Install the [Cloud SDK].
   > *Note:* This is not required in
   > [Cloud Shell]
   > since it already has the Cloud SDK pre-installed.

1. Create a new Google Cloud project via the
   [*New Project* page],
   or via the `gcloud` command line tool.

   ```sh
   export PROJECT_NAME=your-google-cloud-project-id
   gcloud projects create $PROJECT_NAME
   ```

1. [Enable billing].

1. Setup the Cloud SDK to your GCP project.

   ```sh
   gcloud init
   ```

1. [Enable the APIs](https://console.cloud.google.com/flows/enableapi?apiid=dataflow,compute_component,logging,storage_component,storage_api,pubsub,cloudresourcemanager.googleapis.com,cloudscheduler.googleapis.com,appengine.googleapis.com): Dataflow, Compute Engine, Stackdriver Logging, Cloud Storage, Cloud Storage JSON, Pub/Sub, Cloud Scheduler, Cloud Resource Manager, and App Engine.

1. Create a service account JSON key via the
   [*Create service account key* page],
   or via the `gcloud` command line tool.
   Here is how to do it through the *Create service account key* page.

   * From the **Service account** list, select **New service account**.
   * In the **Service account name** field, enter a name.
   * From the **Role** list, select **Project > Owner** **(*)**.
   * Click **Create**. A JSON file that contains your key downloads to your computer.

   Alternatively, you can use `gcloud` through the command line.

   ```sh
   export PROJECT_NAME=$(gcloud config get-value project)
   export SA_NAME=samples
   export IAM_ACCOUNT=$SA_NAME@$PROJECT_NAME.iam.gserviceaccount.com

   # Create the service account.
   gcloud iam service-accounts create $SA_NAME --display-name $SA_NAME

   # Set the role to Project Owner (*).
   gcloud projects add-iam-policy-binding $PROJECT_NAME \
     --member serviceAccount:$IAM_ACCOUNT \
     --role roles/owner

   # Create a JSON file with the service account credentials.
   gcloud iam service-accounts keys create path/to/your/credentials.json \
     --iam-account=$IAM_ACCOUNT
   ```

   > **(*)** *Note:* The **Role** field authorizes your service account to access resources.
   > You can view and change this field later by using the
   > [GCP Console IAM page].
   > If you are developing a production app, specify more granular permissions than **Project > Owner**.
   > For more information, see
   > [Granting roles to service accounts].

   For more information, see
   [Creating and managing service accounts].

1. Set your `GOOGLE_APPLICATION_CREDENTIALS` environment variable to point to your service account key file.

   ```sh
   export GOOGLE_APPLICATION_CREDENTIALS=path/to/your/credentials.json
   ```

1. Create a Cloud Storage bucket.

   ```bash
   export BUCKET_NAME=your-gcs-bucket

   gsutil mb gs://$BUCKET_NAME
   ```

 1. Start a [Google Cloud Scheduler] job that publishes one message to a [Google Cloud Pub/Sub] topic every minute. This will create an [App Engine] app if one has never been created on the project.

    ```bash
    # Create a Pub/Sub topic.
    gcloud pubsub topics create cron-topic

    # Create a Cloud Scheduler job
    gcloud scheduler jobs create pubsub publisher-job --schedule="* * * * *" \
      --topic=cron-topic --message-body="Hello!"

    # Run the job.
    gcloud scheduler jobs run publisher-job
    ```

## Setup

The following instructions will help you prepare your development environment.

1. [Install Python and virtualenv].

1. Clone the `python-docs-samples` repository.

    ```bash
    git clone https://github.com/GoogleCloudPlatform/python-docs-samples.git
    ```

1. Navigate to the sample code directory.

   ```bash
   cd python-docs-samples/pubsub/streaming-analytics
   ```

1. Create a virtual environment and activate it.

  ```bash
  virtualenv env
  source env/bin/activate
  ```
  > Once you are finished with the tutorial, you can deactivate the virtualenv and go back to your global Python environment by running `deactivate`.

1. Install the sample requirements.

  ```bash
  pip install -U -r requirements.txt
  ```

## Streaming Analytics

### Google Cloud Pub/Sub to Google Cloud Storage

* [PubSubToGCS.py](PubSubToGCS.py)

The following example will run a streaming pipeline. It will read messages from a Pub/Sub topic, then window them into fixed-sized intervals, and write one file per window into a GCS location.

+ `--project`: sets the Google Cloud project ID to run the pipeline on
+ `--input_topic`: sets the input Pub/Sub topic to read messages from
+ `--output_path`: sets the output GCS path prefix to write files to
+ `--runner`: specifies the runner to run the pipeline, if not set to `DataflowRunner`, `DirectRunner` is used
+ `--window_size [optional]`: specifies the window size in minutes, defaults to 1.0
+ `--temp_location`: needed for executing the pipeline

```bash
python PubSubToGCS.py \
  --project=$PROJECT_NAME \
  --input_topic=projects/$PROJECT_NAME/topics/$TOPIC_NAME \
  --output_path=gs://$BUCKET_NAME/samples/output \
  --runner=DataflowRunner \
  --window_size=2 \
  --temp_location=gs://$BUCKET_NAME/temp
```

After the job has been submitted, you can check its status in the [GCP Console Dataflow page].

You can also check the output to your GCS bucket using the command line below or in the [GCP Console Storage page]. You may need to wait a few minutes for the files to appear.

```bash
gsutil ls gs://$BUCKET_NAME/samples/
```

## Cleanup

1. Delete the [Google Cloud Scheduler] job.

    ```bash
    gcloud scheduler jobs delete publisher-job
    ```

1. `Ctrl+C` to stop the program in your terminal. Note that this does not actually stop the job if you use `DataflowRunner`.

1.  If you use `DirectRunner`, you can skip this step. Stop the Dataflow job in [GCP Console Dataflow page]. Cancel the job instead of draining it. This may take some minutes.

1. Delete the topic. [Google Cloud Dataflow] will automatically delete the subscription associated with the streaming pipeline when the job is canceled.

   ```bash
   gcloud pubsub topics delete cron-topic
   ```

1. Lastly, to avoid incurring charges to your GCP account for the resources created in this tutorial:

    ```bash
    # Delete only the files created by this sample.
    gsutil -m rm -rf "gs://$BUCKET_NAME/samples/output*"

    # [optional] Remove the Cloud Storage bucket.
    gsutil rb gs://$BUCKET_NAME
    ```

[Apache Beam]: https://beam.apache.org/
[Google Cloud Pub/Sub]: https://cloud.google.com/pubsub/docs/
[Google Cloud Dataflow]: https://cloud.google.com/dataflow/docs/
[Google Cloud Scheduler]: https://cloud.google.com/scheduler/docs/
[App Engine]: https://cloud.google.com/appengine/docs/

[Cloud SDK]: https://cloud.google.com/sdk/docs/
[Cloud Shell]: https://console.cloud.google.com/cloudshell/editor/
[*New Project* page]: https://console.cloud.google.com/projectcreate
[Enable billing]: https://cloud.google.com/billing/docs/how-to/modify-project/
[*Create service account key* page]: https://console.cloud.google.com/apis/credentials/serviceaccountkey/
[GCP Console IAM page]: https://console.cloud.google.com/iam-admin/iam/
[Granting roles to service accounts]: https://cloud.google.com/iam/docs/granting-roles-to-service-accounts/
[Creating and managing service accounts]: https://cloud.google.com/iam/docs/creating-managing-service-accounts/

[Install Python and virtualenv]: https://cloud.google.com/python/setup/

[GCP Console create Dataflow job page]: https://console.cloud.google.com/dataflow/createjob/
[GCP Console Dataflow page]: https://console.cloud.google.com/dataflow/
[GCP Console Storage page]: https://console.cloud.google.com/storage/
