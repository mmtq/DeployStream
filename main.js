const core = require('@actions/core');
const { exec } = require('@actions/exec');

async function run() {
  try {
    // Get environment variables
    const username = core.getInput('SSH_USERNAME', { required: true });
    const ipAddress = core.getInput('SSH_IPADDRESS', { required: true });
    const password = core.getInput('SSH_PASSWORD', { required: true });
    const localPath = core.getInput('LOCAL_PATH', { required: true });
    const remotePath = core.getInput('REMOTE_PATH', { required: true });

    // Mask sensitive information
    core.setSecret(password);

    // Install sshpass
    console.log('Installing sshpass...');
    await exec('sudo apt-get update && sudo apt-get install -y sshpass');

    // Construct the rsync command
    const rsyncCommand = [
      `sshpass -p "${password}" rsync -rv`,
      `-e "ssh -o StrictHostKeyChecking=no"`,
      `"${localPath}"`,
      `"${username}@${ipAddress}:${remotePath}"`,
      `--exclude .git`
    ].join(' ');

    // Log the command (excluding the password for security)
    console.log('Executing command:');
    console.log(rsyncCommand.replace(password, '*****'));

    // Execute the rsync command
    await exec(rsyncCommand);

    console.log('Deployment completed successfully.');
  } catch (error) {
    core.setFailed(`Deployment failed: ${error.message}`);
  }
}

run();
