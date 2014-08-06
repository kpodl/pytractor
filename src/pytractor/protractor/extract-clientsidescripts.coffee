'use strict'

EXTRACTED_DIR = 'extracted'

fs = require 'fs'
client_side_scripts = require './node_modules/protractor/lib/clientsidescripts.js'

for name, script of client_side_scripts
    console.log "Extracting '#{name}'"
    fs.writeFileSync "#{EXTRACTED_DIR}/#{name}.js", script
    console.log "  #{name} extracted successfully."
