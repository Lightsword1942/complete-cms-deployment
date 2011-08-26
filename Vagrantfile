Vagrant::Config.run do |config|

    config.vm.define :loadbal do |config|
      config.vm.box = "lucid32"
      config.vm.network('33.33.33.1')
      config.vm.customize do |vm|
          vm.memory_size = 256
      end
    end

    config.vm.define :web1 do |config|
      config.vm.box = "lucid32"
      config.vm.network('33.33.33.10')
      config.vm.customize do |vm|
          vm.memory_size = 256
      end
    end

    config.vm.define :web2 do |config|
      config.vm.box = "lucid32"
      config.vm.network('33.33.33.11')
      config.vm.customize do |vm|
          vm.memory_size = 256
      end
    end
    
    config.vm.define :db do |config|
      config.vm.box = "lucid32"
      config.vm.network('33.33.33.20')
      config.vm.customize do |vm|
          vm.memory_size = 256
      end
    end
    
    config.vm.define :dbfailover do |config|
      config.vm.box = "lucid32"
      config.vm.network('33.33.33.21')
      config.vm.customize do |vm|
          vm.memory_size = 256
      end
    end

    config.vm.define :rabbitmq do |config|
      config.vm.box = "lucid32"
      config.vm.network('33.33.33.30')
      config.vm.customize do |vm|
          vm.memory_size = 256
      end
    end

    config.vm.define :celery do |config|
      config.vm.box = "lucid32"
      config.vm.network('33.33.33.31')
      config.vm.customize do |vm|
          vm.memory_size = 256
      end
    end

    config.vm.define :memcached do |config|
      config.vm.box = "lucid32"
      config.vm.network('33.33.33.40')
      config.vm.customize do |vm|
          vm.memory_size = 256
      end
    end

    config.vm.define :solr do |config|
      config.vm.box = "lucid32"
      config.vm.network('33.33.33.50')
      config.vm.customize do |vm|
          vm.memory_size = 256
      end
    end    
   
end
