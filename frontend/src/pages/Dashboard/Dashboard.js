import React, { useState, useEffect } from 'react';
import { Row, Col, Card, Statistic } from 'antd';
import { Line } from '@ant-design/plots';
import { taskAPI, proxyAPI } from '../../services/api';

const Dashboard = () => {
  const [taskStats, setTaskStats] = useState({
    total: 0,
    running: 0,
    completed: 0,
    failed: 0,
  });
  const [proxyStats, setProxyStats] = useState({
    total: 0,
    active: 0,
  });

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const [tasks, proxies] = await Promise.all([
          taskAPI.getTasks(),
          proxyAPI.getProxyStats(),
        ]);

        // 计算任务统计
        const stats = tasks.reduce(
          (acc, task) => {
            acc.total += 1;
            acc[task.status] = (acc[task.status] || 0) + 1;
            return acc;
          },
          { total: 0, running: 0, completed: 0, failed: 0 }
        );
        setTaskStats(stats);

        // 设置代理统计
        setProxyStats(proxies);
      } catch (error) {
        console.error('Failed to fetch stats:', error);
      }
    };

    fetchStats();
  }, []);

  // 任务执行趋势数据
  const taskTrendData = {
    data: [
      { date: '2024-01', tasks: 3 },
      { date: '2024-02', tasks: 4 },
      { date: '2024-03', tasks: 6 },
      { date: '2024-04', tasks: 8 },
      { date: '2024-05', tasks: 7 },
      { date: '2024-06', tasks: 9 },
    ],
    xField: 'date',
    yField: 'tasks',
    smooth: true,
  };

  return (
    <div>
      <Row gutter={16}>
        <Col span={6}>
          <Card>
            <Statistic title="总任务数" value={taskStats.total} />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic title="运行中任务" value={taskStats.running} />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic title="完成任务" value={taskStats.completed} />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic title="失败任务" value={taskStats.failed} />
          </Card>
        </Col>
      </Row>

      <Row gutter={16} style={{ marginTop: 16 }}>
        <Col span={12}>
          <Card title="任务执行趋势">
            <Line {...taskTrendData} />
          </Card>
        </Col>
        <Col span={12}>
          <Card title="代理状态">
            <Row gutter={16}>
              <Col span={12}>
                <Statistic title="总代理数" value={proxyStats.total} />
              </Col>
              <Col span={12}>
                <Statistic title="活跃代理" value={proxyStats.active} />
              </Col>
            </Row>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Dashboard;
