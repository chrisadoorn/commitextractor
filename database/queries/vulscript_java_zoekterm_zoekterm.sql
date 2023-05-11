set schema 'test';

INSERT INTO java_zoekterm (zoekterm,categorie,package,opmerking) VALUES
	 ('synchronized','keywords',NULL,'(code block) or (methods)'),
	 ('volatile','keywords',NULL,NULL),
	 ('Runnable','interfaces','java.lang',NULL),
	 ('BlockingDeque','interfaces','java.util.concurrent',NULL),
	 ('BlockingQueue','interfaces','java.util.concurrent',NULL),
	 ('Callable','interfaces','java.util.concurrent',NULL),
	 ('CompletableFuture.AsynchronousCompletionTask','interfaces','java.util.concurrent',NULL),
	 ('CompletionService','interfaces','java.util.concurrent',NULL),
	 ('CompletionStage','interfaces','java.util.concurrent',NULL),
	 ('ConcurrentMap','interfaces','java.util.concurrent',NULL);
INSERT INTO java_zoekterm (zoekterm,categorie,package,opmerking) VALUES
	 ('ConcurrentNavigableMap','interfaces','java.util.concurrent',NULL),
	 ('Delayed','interfaces','java.util.concurrent',NULL),
	 ('Executor','interfaces','java.util.concurrent',NULL),
	 ('ExecutorService','interfaces','java.util.concurrent',NULL),
	 ('ForkJoinPool.ForkJoinWorkerThreadFactory','interfaces','java.util.concurrent',NULL),
	 ('ForkJoinPool.ManagedBlocker','interfaces','java.util.concurrent',NULL),
	 ('Future','interfaces','java.util.concurrent',NULL),
	 ('RejectedExecutionHandler','interfaces','java.util.concurrent',NULL),
	 ('RunnableFuture','interfaces','java.util.concurrent',NULL),
	 ('RunnableScheduledFuture','interfaces','java.util.concurrent',NULL);
INSERT INTO java_zoekterm (zoekterm,categorie,package,opmerking) VALUES
	 ('ScheduledExecutorService','interfaces','java.util.concurrent',NULL),
	 ('ThreadFactory','interfaces','java.util.concurrent',NULL),
	 ('TransferQueue','interfaces','java.util.concurrent',NULL),
	 ('Condition','interfaces','java.util.concurrent',NULL),
	 ('Lock','interfaces','java.util.concurrent',NULL),
	 ('ReadWriteLock','interfaces','java.util.concurrent',NULL),
	 ('AbstractExecutorService','classes','java.util.concurrent',NULL),
	 ('ArrayBlockingQueue','classes','java.util.concurrent',NULL),
	 ('CompletableFuture','classes','java.util.concurrent',NULL),
	 ('ConcurrentHashMap','classes','java.util.concurrent',NULL);
INSERT INTO java_zoekterm (zoekterm,categorie,package,opmerking) VALUES
	 ('ConcurrentHashMap.KeySetView','classes','java.util.concurrent',NULL),
	 ('ConcurrentLinkedDeque','classes','java.util.concurrent',NULL),
	 ('ConcurrentLinkedQueue','classes','java.util.concurrent',NULL),
	 ('ConcurrentSkipListMap','classes','java.util.concurrent',NULL),
	 ('ConcurrentSkipListSet','classes','java.util.concurrent',NULL),
	 ('CopyOnWriteArrayList','classes','java.util.concurrent',NULL),
	 ('CopyOnWriteArraySet','classes','java.util.concurrent',NULL),
	 ('CountDownLatch','classes','java.util.concurrent',NULL),
	 ('CountedCompleter','classes','java.util.concurrent',NULL),
	 ('CyclicBarrier','classes','java.util.concurrent',NULL);
INSERT INTO java_zoekterm (zoekterm,categorie,package,opmerking) VALUES
	 ('DelayQueue','classes','java.util.concurrent',NULL),
	 ('Exchanger','classes','java.util.concurrent',NULL),
	 ('ExecutorCompletionService','classes','java.util.concurrent',NULL),
	 ('Executors','classes','java.util.concurrent',NULL),
	 ('ForkJoinPool','classes','java.util.concurrent',NULL),
	 ('ForkJoinTask','classes','java.util.concurrent',NULL),
	 ('ForkJoinWorkerThread','classes','java.util.concurrent',NULL),
	 ('FutureTask','classes','java.util.concurrent',NULL),
	 ('LinkedBlockingDeque','classes','java.util.concurrent',NULL),
	 ('LinkedBlockingQueue','classes','java.util.concurrent',NULL);
INSERT INTO java_zoekterm (zoekterm,categorie,package,opmerking) VALUES
	 ('LinkedTransferQueue','classes','java.util.concurrent',NULL),
	 ('Phaser','classes','java.util.concurrent',NULL),
	 ('PriorityBlockingQueue','classes','java.util.concurrent',NULL),
	 ('RecursiveAction','classes','java.util.concurrent',NULL),
	 ('RecursiveTask','classes','java.util.concurrent',NULL),
	 ('ScheduledThreadPoolExecutor','classes','java.util.concurrent',NULL),
	 ('Semaphore','classes','java.util.concurrent',NULL),
	 ('SynchronousQueue','classes','java.util.concurrent',NULL),
	 ('ThreadLocalRandom','classes','java.util.concurrent',NULL),
	 ('ThreadPoolExecutor','classes','java.util.concurrent',NULL);
INSERT INTO java_zoekterm (zoekterm,categorie,package,opmerking) VALUES
	 ('ThreadPoolExecutor.AbortPolicy','classes','java.util.concurrent',NULL),
	 ('ThreadPoolExecutor.CallerRunsPolicy','classes','java.util.concurrent',NULL),
	 ('ThreadPoolExecutor.DiscardOldestPolicy','classes','java.util.concurrent',NULL),
	 ('ThreadPoolExecutor.DiscardPolicy','classes','java.util.concurrent',NULL),
	 ('VarHandle','classes','java.lang.invoke',NULL),
	 ('AtomicBoolean','classes','java.util.concurrent.atomic',NULL),
	 ('AtomicInteger','classes','java.util.concurrent.atomic',NULL),
	 ('AtomicLong','classes','java.util.concurrent.atomic',NULL),
	 ('AbstractOwnableSynchronizer','classes','java.util.concurrent.locks',NULL),
	 ('AbstractQueuedLongSynchronizer','classes','java.util.concurrent.locks',NULL);
INSERT INTO java_zoekterm (zoekterm,categorie,package,opmerking) VALUES
	 ('AbstractQueuedSynchronizer','classes','java.util.concurrent.locks',NULL),
	 ('LockSupport','classes','java.util.concurrent.locks',NULL),
	 ('ReentrantLock','classes','java.util.concurrent.locks',NULL),
	 ('ReentrantReadWriteLock','classes','java.util.concurrent.locks',NULL),
	 ('ReentrantReadWriteLock.ReadLock','classes','java.util.concurrent.locks',NULL),
	 ('ReentrantReadWriteLock.WriteLock','classes','java.util.concurrent.locks',NULL),
	 ('Collections.synchronizedCollection()  	','classes','java.util.collections ',NULL),
	 ('Collections.synchronizedList()  	','classes','java.util.collections ',NULL),
	 ('Collections.synchronizedMap()  	','classes','java.util.collections ',NULL),
	 ('Collections.synchronizedSet()  	','classes','java.util.collections ',NULL);
INSERT INTO java_zoekterm (zoekterm,categorie,package,opmerking) VALUES
	 ('Collections.synchronizedSortedMap()  	','classes','java.util.collections ',NULL),
	 ('Collections.synchronizedSortedSet()  	','classes','java.util.collections ',NULL),
	 ('io.reactivex.rxjava2','libraries',NULL,'RxJava'),
	 ('org.awaitility','libraries',NULL,'Awaitility'),
	 ('io.projectreacto','libraries',NULL,'ProjectReactor'),
	 ('com.lmax','libraries',NULL,'Disruptor');

	
-- vul zoekterm vanuit java zoektermen lijst	
insert into zoekterm ( extensie, zoekwoord)
select '.java', j.zoekterm  from java_zoekterm j;