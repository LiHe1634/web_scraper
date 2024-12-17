import React, { useState, useEffect } from 'react';
import { Table, Button, Space, Tag, Modal, message } from 'antd';
import { PlusOutlined, PlayCircleOutlined, DeleteOutlined, EditOutlined } from '@ant-design/icons';
import { taskAPI } from '../../services/api';
import TaskForm from './TaskForm';

const TaskList = () => {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingTask, setEditingTask] = useState(null);

  const fetchTasks = async () => {
    setLoading(true);
    try {
      const data = await taskAPI.getTasks();
      setTasks(data);
    } catch (error) {
      message.error('获取任务列表失败');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  const handleStartTask = async (id) => {
    try {
      await taskAPI.startTask(id);
      message.success('任务已启动');
      fetchTasks();
    } catch (error) {
      message.error('启动任务失败');
    }
  };

  const handleDeleteTask = async (id) => {
    Modal.confirm({
      title: '确认删除',
      content: '确定要删除这个任务吗？',
      onOk: async () => {
        try {
          await taskAPI.deleteTask(id);
          message.success('任务已删除');
          fetchTasks();
        } catch (error) {
          message.error('删除任务失败');
        }
      },
    });
  };

  const columns = [
    {
      title: '任务名称',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'URL',
      dataIndex: 'url',
      key: 'url',
      ellipsis: true,
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status) => {
        const colors = {
          pending: 'blue',
          running: 'green',
          completed: 'success',
          failed: 'error',
        };
        return <Tag color={colors[status]}>{status.toUpperCase()}</Tag>;
      },
    },
    {
      title: '上次运行',
      dataIndex: 'last_run',
      key: 'last_run',
    },
    {
      title: '操作',
      key: 'action',
      render: (_, record) => (
        <Space size="middle">
          <Button
            type="primary"
            icon={<PlayCircleOutlined />}
            onClick={() => handleStartTask(record.id)}
            disabled={record.status === 'running'}
          >
            运行
          </Button>
          <Button
            icon={<EditOutlined />}
            onClick={() => {
              setEditingTask(record);
              setModalVisible(true);
            }}
          >
            编辑
          </Button>
          <Button
            danger
            icon={<DeleteOutlined />}
            onClick={() => handleDeleteTask(record.id)}
          >
            删除
          </Button>
        </Space>
      ),
    },
  ];

  return (
    <div>
      <div style={{ marginBottom: 16 }}>
        <Button
          type="primary"
          icon={<PlusOutlined />}
          onClick={() => {
            setEditingTask(null);
            setModalVisible(true);
          }}
        >
          新建任务
        </Button>
      </div>
      <Table
        columns={columns}
        dataSource={tasks}
        rowKey="id"
        loading={loading}
      />
      <TaskForm
        visible={modalVisible}
        onCancel={() => {
          setModalVisible(false);
          setEditingTask(null);
        }}
        onSuccess={() => {
          setModalVisible(false);
          setEditingTask(null);
          fetchTasks();
        }}
        initialValues={editingTask}
      />
    </div>
  );
};

export default TaskList;
