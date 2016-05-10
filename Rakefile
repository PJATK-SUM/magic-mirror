require 'sshkit'
require 'date'

APP_NAME="magic-mirror"
APP_PATH = "/var/www/#{APP_NAME}"
RELEASES_PATH = "#{APP_PATH}/releases"
SHARED_PATH = "#{APP_PATH}/shared"
SERVER = "root@46.101.231.214"
KEEP_RELEASES = 5

namespace :meteor do
  include SSHKit::DSL

  task :generate_paths do
    RELEASE_NUMBER = DateTime.now.strftime("%Y%m%d%H%M%S")
    RELEASE_PATH = "#{RELEASES_PATH}/#{RELEASE_NUMBER}"
    TEMP_PATH = "/tmp/#{APP_NAME}-#{RELEASE_NUMBER}"
    BUNDLE = "#{TEMP_PATH}/#{APP_NAME}.tar.gz"
  end

  task :prepare do
    on SERVER do |host|
      unless test "[ -d #{RELEASES_PATH} ]"
        execute :mkdir, "-p", RELEASES_PATH
      end

      unless test "[ -d #{SHARED_PATH} ]"
        execute :mkdir, "-p", SHARED_PATH
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

  task :cleanup do
    sh "rm #{BUNDLE}"
    sh "rmdir #{TEMP_PATH}"

    on SERVER do |host|
      releases = capture(:ls, "-xtr", RELEASES_PATH).split

      if releases.count >= KEEP_RELEASES
        directories = (releases - releases.last(KEEP_RELEASES))
        if directories.any?
          directories_str = directories.map do |release|
            "#{RELEASES_PATH}/#{release}"
          end.select{ |path| path != "/" }.join(" ")
          execute :rm, "-rf", directories_str
        end
      end
    end
  end

  desc "Builds a bundle, deploys the app and restarts the server"
  task :deploy => [:generate_paths, :prepare, :bundle, :upload, :link, :cleanup] do
    on SERVER do |host|
      within APP_PATH do
        execute "./start.sh"
      end
    end
  end
end
