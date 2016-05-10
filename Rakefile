require 'sshkit'

APP_NAME="magic-mirror"
APP_PATH = "/var/www/#{APP_NAME}"
SERVER = "root@46.101.231.214"

namespace :meteor do
  include SSHKit::DSL

  task :generate_paths do
    RELEASE_NUMBER = DateTime.now.strftime("%Y%m%d%H%M%S")
    RELEASE_PATH = "#{APP_PATH}/releases/#{RELEASE_NUMBER}"
    TEMP_PATH = "/tmp/#{APP_NAME}-#{RELEASE_NUMBER}"
    BUNDLE = "#{TEMP_PATH}/#{APP_NAME}.tar.gz"
  end

  task :prepare do
    on SERVER do |host|
      unless test "[ -d #{APP_PATH}/releases ]"
        execute :mkdir, "-p", "#{APP_PATH}/releases"
      end

      unless test "[ -d #{APP_PATH}/shared]"
        execute :mkdir, "-p", "#{APP_PATH}/shared"
      end

      upload! "start.sh", APP_PATH
    end
  end

  task :bundle do
    puts "Building Meteor app..."
    sh "meteor build --architecture=os.linux.x86_64 #{TEMP_PATH}"
  end

  task :upload do
    on SERVER do |host|
      unless test "[ -d #{APP_PATH}/releases ]"
        execute :mkdir, "-p", "#{APP_PATH}/releases"
      end

      execute :mkdir, "-p", "#{RELEASE_PATH}/bundle"
      upload! BUNDLE, "#{RELEASE_PATH}/bundle.tar.gz"
    end
  end

  task :link do
    on SERVER do |host|
      if test "[ -h #{APP_PATH}/current ]"
        execute :rm, "#{APP_PATH}/current"
      end

      execute :ln, "-s", RELEASE_PATH, "#{APP_PATH}/current"
    end
  end

  desc "Builds a bundle, deploys the app and restarts the server"
  task :deploy => [:generate_paths, :prepare, :bundle, :upload, :link] do
    on SERVER do |host|
      within APP_PATH do
        execute "./start.sh"
      end
    end
  end
end
