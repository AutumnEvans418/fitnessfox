
#cp -r . temp

#zip build.zip temp

# Change these values to the ones used to create the App Service.
RESOURCE_GROUP_NAME='autumnfox418_rg_1137'
APP_SERVICE_NAME='FitnessFox'

az webapp deploy --name $APP_SERVICE_NAME --resource-group $RESOURCE_GROUP_NAME --src-path build.zip

#rm -r temp