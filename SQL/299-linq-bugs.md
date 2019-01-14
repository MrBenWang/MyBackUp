# linq的开发中的bug

- 先用where执行运算过滤，然后再排序

```csharp
RoomRepository.Entities.Where(
    room => room.Code == code && (!String.IsNullOrEmpty(status) ? room.STATUS == status : true))
// if i use order by function it will raise NullReferenceException
.OrderBy(room => room.ROOM_NO);
```

https://bugs.mysql.com/bug.php?id=77735
解决办法：String.IsNullOrEmpty 方法提取出来，或者不允许为NULL。