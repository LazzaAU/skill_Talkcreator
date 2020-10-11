module.exports = function(RED) {
	function runtalkcreator(config) {
		RED.nodes.createNode(this, config);
	}

	RED.nodes.registerType('runtalkcreator', runtalkcreator);
}