import rclpy
from rclpy.node import Node

class Generic(Node): 
    def __init__(self):
        super().__init__('node_name') 
        self.get_logger().info('Node has been started.')


def main(args=None):
    rclpy.init(args=args) 
    generic_node = Generic() 
    rclpy.spin(generic_node) 
    generic_node.destroy_node() 
    rclpy.shutdown()

if __name__ == '__main__':
    main()


