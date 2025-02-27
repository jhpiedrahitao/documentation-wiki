# Permissions and Security in Amazon Augmented AI<a name="a2i-permissions-security"></a>

When using Amazon Augmented AI \(Amazon A2I\) to create a human review workflow for your ML/AI application, you create and configure *resources* in Amazon SageMaker such as a human workforce and worker task templates\. To configure and start a human loop, you either integrate Amazon A2I with other AWS services such as Amazon Textract or Amazon Rekognition, or use the Amazon Augmented AI Runtime API\. To create a human review workflow and start a human loop, you must attach certain policies to your AWS Identity and Access Management \(IAM\) role or user\. Specifically: 
+ When you start a human loop using image input data on or after January 12th, 2020, you must add a CORS header policy to the Amazon S3 bucket that contains your input data\. See [CORS Permission Requirement](#a2i-cors-update) to learn more\. 
+ When you create a flow definition, you need to provide a role that grants Amazon A2I permission to access Amazon S3 both for reading objects that are rendered in a human task UI and for writing the results of the human review\. 

  This role must also have a trust policy attached to give SageMaker permission to assume the role\. This allows Amazon A2I to perform actions in accordance with permissions that you attach to the role\. 

  See [Add Permissions to the IAM Role Used to Create a Flow Definition](#a2i-human-review-permissions-s3) for example policies that you can modify and attach to the role you use to create a flow definition\. These are the policies that are attached to the IAM role that is created in the **Human review workflows** section of the Amazon A2I area of the SageMaker console\. 
+ To create and start human loops, you either use an API operation from a built\-in task type \(such as `DetectModerationLabel` or `AnalyzeDocument`\) or the Amazon A2I Runtime API operation `StartHumanLoop` in a custom ML application\. You need to attach the `AmazonAugmentedAIFullAccess` managed policy to the user that invokes these API operations to grant permission to these services to use Amazon A2I operations\. To learn how, see [Create a User That Can Invoke Amazon A2I API Operations](#create-user-grants)\.

  This policy does *not* grant permission to invoke the API operations of the AWS service associated with built\-in task types\. For example, `AmazonAugmentedAIFullAccess` does not grant permission to call the Amazon Rekognition `DetectModerationLabel` API operation or Amazon Textract `AnalyzeDocument` API operation\. You can use the more general policy, `AmazonAugmentedAIIntegratedAPIAccess`, to grant these permissions\. For more information, see [Create a User With Permissions to Invoke Amazon A2I, Amazon Textract, and Amazon Rekognition API Operations](#a2i-grant-general-permission)\. This is a good option when you want to grant a user broad permissions to use Amazon A2I and integrated AWS services' API operations\. 

  If you want to configure more granular permissions, see [Amazon Rekognition Identity\-Based Policy Examples](https://docs.aws.amazon.com/rekognition/latest/dg/security_iam_id-based-policy-examples.html) and [Amazon Textract Identity\-Based Policy Examples](https://docs.aws.amazon.com/textract/latest/dg/security_iam_id-based-policy-examples.html) for identity\-based policies you can use to grant permission to use these individual services\.
+ To preview your custom worker task UI template, you need an IAM role with permissions to read Amazon S3 objects that get rendered on your user interface\. See a policy example in [Enable Worker Task Template Previews ](#permissions-for-worker-task-templates-augmented-ai)\.

**Topics**
+ [CORS Permission Requirement](#a2i-cors-update)
+ [Add Permissions to the IAM Role Used to Create a Flow Definition](#a2i-human-review-permissions-s3)
+ [Create a User That Can Invoke Amazon A2I API Operations](#create-user-grants)
+ [Create a User With Permissions to Invoke Amazon A2I, Amazon Textract, and Amazon Rekognition API Operations](#a2i-grant-general-permission)
+ [Enable Worker Task Template Previews](#permissions-for-worker-task-templates-augmented-ai)
+ [Using Amazon A2I with AWS KMS Encrypted Buckets](#a2i-kms-encryption)
+ [Additional Permissions and Security Resources](#additional-security-resources-augmented-ai)

## CORS Permission Requirement<a name="a2i-cors-update"></a>

Earlier in 2020, widely used browsers like Chrome and Firefox changed their default behavior for rotating images based on image metadata, referred to as [EXIF data](https://en.wikipedia.org/wiki/Exif)\. Previously, images would always display in browsers exactly how they are stored on disk, which is typically unrotated\. After the change, images now rotate according to a piece of image metadata called *orientation value*\. This has important implications for the entire machine learning \(ML\) community\. For example, if the EXIF orientation is not considered, applications that are used to annotate images may display images in unexpected orientations and result in incorrect labels\. 

Starting with Chrome 89, AWS can no longer automatically prevent the rotation of images because the web standards group W3C has decided that the ability to control rotation of images violates the web’s Same\-Origin Policy\. Therefore, to ensure human workers annotate your input images in a predictable orientation when you submit requests to create a human loop, you must add a CORS header policy to the S3 buckets that contain your input images\.

**Important**  
If you do not add a CORS configuration to the S3 buckets that contains your input data, human review tasks for those input data objects fail\.

You can add a CORS policy to an S3 bucket that contains input data in the Amazon S3 console\. To set the required CORS headers on the S3 bucket that contains your input images in the S3 console, follow the directions detailed in [How do I add cross\-domain resource sharing with CORS?](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/add-cors-configuration.html)\. Use the following CORS configuration code for the buckets that host your images\. If you use the Amazon S3 console to add the policy to your bucket, you must use the JSON format\.

**JSON**

```
[{
   "AllowedHeaders": [],
   "AllowedMethods": ["GET"],
   "AllowedOrigins": ["*"],
   "ExposeHeaders": []
}]
```

**XML**

```
<CORSConfiguration>
 <CORSRule>
   <AllowedOrigin>*</AllowedOrigin>
   <AllowedMethod>GET</AllowedMethod>
 </CORSRule>
</CORSConfiguration>
```

The following GIF demonstrates the instructions found in the Amazon S3 documentation to add a CORS header policy using the Amazon S3 console\.

![\[Image NOT FOUND\]](http://docs.aws.amazon.com/sagemaker/latest/dg/images/sms/gifs/cors-config.gif)

## Add Permissions to the IAM Role Used to Create a Flow Definition<a name="a2i-human-review-permissions-s3"></a>

To create a flow definition, attach the policies in this section to the role that you use when creating a human review workflow in the SageMaker console, or when using the `CreateFlowDefinition` API operation\.
+ If you are using the console to create a human review workflow, enter the role Amazon Resource Name \(ARN\) in the **IAM role** field when [creating a human review workflow in the console](https://docs.aws.amazon.com/sagemaker/latest/dg/create-human-review-console.html)\. 
+ When creating a flow definition using the API, attach these policies to the role that is passed to the `RoleArn` parameter of the `CreateFlowDefinition` operation\. 

When you create a human review workflow \(flow definition\), Amazon A2I invokes Amazon S3 to complete your task\. To grant Amazon A2I permission to retrieve and store your files in your Amazon S3 bucket, create the following policy and attach it to your role\. For example, if the images, documents, and other files that you are sending for human review are stored in an S3 bucket named `my_input_bucket`, and if you want the human reviews to be stored in a bucket named `my_output_bucket`, create the following policy\. 

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::my_input_bucket/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject"
            ],
            "Resource": [
                "arn:aws:s3:::my_output_bucket/*"
            ]
        }
    ]
}
```

In addition, the IAM role must have the following trust policy to give SageMaker permission to assume the role\. To learn more about IAM trust policies, see [Resource\-Based Policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#policies_resource-based) section of **Policies and Permissions** in the *AWS Identity and Access Management* documentation\.

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowSageMakerToAssumeRole",
      "Effect": "Allow",
      "Principal": {
        "Service": "sagemaker.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

For more information about creating and managing IAM roles and policies, see the following topics in the *AWS Identity and Access Management User Guide*: 
+ To create an IAM role, see [Creating a Role to Delegate Permissions to an IAM User](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user.html)\. 
+ To learn how to create IAM policies, see [Creating IAM Policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_create.html)\. 
+ To learn how to attach an IAM policy to a role, see [Adding and Removing IAM Identity Permissions](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_manage-attach-detach.html)\.

## Create a User That Can Invoke Amazon A2I API Operations<a name="create-user-grants"></a>

To use Amazon A2I to create and start human loops for Amazon Rekognition, Amazon Textract, or the Amazon A2I runtime API, you must use a user that has permissions to invoke Amazon A2I operations\. To do this, use the IAM console to attach the [https://console.aws.amazon.com/iam/home?region=us-east-2#/policies/arn:aws:iam::aws:policy/AmazonAugmentedAIFullAccess$jsonEditor](https://console.aws.amazon.com/iam/home?region=us-east-2#/policies/arn:aws:iam::aws:policy/AmazonAugmentedAIFullAccess$jsonEditor) managed policy to a new or existing user\. 

This policy grants permission to a user to invoke API operations from the SageMaker API for flow definition creation and management and the Amazon Augmented AI Runtime API for human loop creation and management\. To learn more about these API operations, see [Use APIs in Amazon Augmented AI](https://docs.aws.amazon.com/sagemaker/latest/dg/a2i-api-references.html)\.

`AmazonAugmentedAIFullAccess` does not grant permissions to use Amazon Rekognition or Amazon Textract API operations\. 

**Note**  
You can also attach the `AmazonAugmentedAIFullAccess` policy to an IAM role that is used to create and start a human loop\. 

To provide access, add permissions to your users, groups, or roles:
+ Users and groups in AWS IAM Identity Center \(successor to AWS Single Sign\-On\):

  Create a permission set\. Follow the instructions in [Create a permission set](https://docs.aws.amazon.com/singlesignon/latest/userguide/howtocreatepermissionset.html) in the *AWS IAM Identity Center \(successor to AWS Single Sign\-On\) User Guide*\.
+ Users managed in IAM through an identity provider:

  Create a role for identity federation\. Follow the instructions in [Creating a role for a third\-party identity provider \(federation\)](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-idp.html) in the *IAM User Guide*\.
+ IAM users:
  + Create a role that your user can assume\. Follow the instructions in [Creating a role for an IAM user](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user.html) in the *IAM User Guide*\.
  + \(Not recommended\) Attach a policy directly to a user or add a user to a user group\. Follow the instructions in [Adding permissions to a user \(console\)](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_change-permissions.html#users_change_permissions-add-console) in the *IAM User Guide*\.

For more information, see [Adding and Removing IAM Identity Permissions](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_manage-attach-detach.html) in the *AWS Identity and Access Management User Guide*\.

## Create a User With Permissions to Invoke Amazon A2I, Amazon Textract, and Amazon Rekognition API Operations<a name="a2i-grant-general-permission"></a>

To create a user that has permission to invoke the API operations used by the built\-in task types \(that is, `DetectModerationLables` for Amazon Rekognition and `AnalyzeDocument` for Amazon Textract\) and permission to use all Amazon A2I API operations, attach the IAM managed policy, `AmazonAugmentedAIIntegratedAPIAccess`\. You may want to use this policy when you want to grant broad permissions to a user using Amazon A2I with more than one task type\. To learn more about these API operations, see [Use APIs in Amazon Augmented AI](https://docs.aws.amazon.com/sagemaker/latest/dg/a2i-api-references.html)\.

**Note**  
You can also attach the `AmazonAugmentedAIIntegratedAPIAccess` policy to an IAM role that is used to create and start a human loop\. 

To provide access, add permissions to your users, groups, or roles:
+ Users and groups in AWS IAM Identity Center \(successor to AWS Single Sign\-On\):

  Create a permission set\. Follow the instructions in [Create a permission set](https://docs.aws.amazon.com/singlesignon/latest/userguide/howtocreatepermissionset.html) in the *AWS IAM Identity Center \(successor to AWS Single Sign\-On\) User Guide*\.
+ Users managed in IAM through an identity provider:

  Create a role for identity federation\. Follow the instructions in [Creating a role for a third\-party identity provider \(federation\)](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-idp.html) in the *IAM User Guide*\.
+ IAM users:
  + Create a role that your user can assume\. Follow the instructions in [Creating a role for an IAM user](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user.html) in the *IAM User Guide*\.
  + \(Not recommended\) Attach a policy directly to a user or add a user to a user group\. Follow the instructions in [Adding permissions to a user \(console\)](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_change-permissions.html#users_change_permissions-add-console) in the *IAM User Guide*\.

For more information, see [Adding and Removing IAM Identity Permissions](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_manage-attach-detach.html) in the *AWS Identity and Access Management User Guide*\.

## Enable Worker Task Template Previews<a name="permissions-for-worker-task-templates-augmented-ai"></a>

To customize the interface and instructions that your workers see when working on your tasks, you create a worker task template\. You can create the template using the [https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_CreateHumanTaskUi.html](https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_CreateHumanTaskUi.html) operation or the SageMaker console\. 

To preview your template, you need an IAM role with the following permissions to read Amazon S3 objects that get rendered on your user interface\. 

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::my_input_bucket/*"
            ]
        }
    ]
}
```

For Amazon Rekognition and Amazon Textract task types, you can preview your template using the Amazon Augmented AI section of the SageMaker console\. For custom task types, you preview your template by invoking the [https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_RenderUiTemplate.html](https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_RenderUiTemplate.html) operation\. To preview your template, follow the instructions for your task type:
+  Amazon Rekognition and Amazon Textract task types – In the SageMaker console, use the role's Amazon Resource Name \(ARN\) in the procedure documented in [Create a Worker Task Template](a2i-worker-template-console.md#a2i-create-worker-template-console)\.
+ Custom task types – In the `RenderUiTemplate` operation, use the role's ARN in the `RoleArn` parameter\.

## Using Amazon A2I with AWS KMS Encrypted Buckets<a name="a2i-kms-encryption"></a>

If you specify an AWS Key Management Service \(AWS KMS\) customer managed key to encrypt output data in `OutputConfig` of [https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_CreateFlowDefinition.html](https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_CreateFlowDefinition.html), you must add an IAM policy similar to the following to that key\. This policy gives the IAM execution role that you use to create your human loops permission to use this key to perform all of the actions listed in `"Action"`\. To learn more about these actions, see [AWS KMS permissions](https://docs.aws.amazon.com/kms/latest/developerguide/kms-api-permissions-reference.html) in the AWS Key Management Service Developer Guide\.

To use this policy, replace the IAM service\-role ARN in `"Principal"` with the ARN of the execution role you use to create the human review workflow \(flow definition\)\. When you create a labeling job using `CreateFlowDefinition`, this is the ARN you specify for [https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_CreateLabelingJob.html#sagemaker-CreateLabelingJob-request-RoleArn](https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_CreateLabelingJob.html#sagemaker-CreateLabelingJob-request-RoleArn)\. Note that you cannot provide a `KmsKeyId` when you create a flow definition in the console\.

```
{
    "Sid": "AllowUseOfKmsKey",
    "Effect": "Allow",
    "Principal": {
        "AWS": "arn:aws:iam::111122223333:role/service-role/example-role"
    },
    "Action": [
        "kms:Encrypt",
        "kms:Decrypt",
        "kms:ReEncrypt*",
        "kms:GenerateDataKey*",
        "kms:DescribeKey"
    ],
    "Resource": "*"
}
```

## Additional Permissions and Security Resources<a name="additional-security-resources-augmented-ai"></a>
+ [Control Access to SageMaker Resources by Using Tags](security_iam_id-based-policy-examples.md#access-tag-policy)\.
+ [SageMaker Identity\-Based Policies](security_iam_service-with-iam.md#security_iam_service-with-iam-id-based-policies)
+ [Control Creation of SageMaker Resources with Condition Keys](security_iam_id-based-policy-examples.md#sagemaker-condition-examples)
+ [Amazon SageMaker API Permissions: Actions, Permissions, and Resources Reference](api-permissions-reference.md)
+ [Security in Amazon SageMaker](security.md)