namespace :meteor do
  desc "Uploads the Meteor bundle to the server"
  task :upload do
    on hosts do |host|
      upload! "bundle.tar.gz" 
    end
  end
end
