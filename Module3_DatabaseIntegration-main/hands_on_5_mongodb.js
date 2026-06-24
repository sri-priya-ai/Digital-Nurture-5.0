
// 1. Show all databases
show dbs


// 2. Switch to database
use college_nosql


// 3. Create Collection
db.createCollection("feedback")


// 4. Insert First Batch of Documents
db.feedback.insertMany([
  {
    student_id: 1,
    course_code: "CS101",
    semester: "2022-ODD",
    rating: 5,
    comments: "Excellent teaching",
    tags: ["challenging", "well-structured", "good-examples"],
    submitted_at: new Date(),
    attachments: [{ filename: "notes.pdf", size_kb: 240 }]
  },
  {
    student_id: 2,
    course_code: "CS101",
    semester: "2022-ODD",
    rating: 4,
    comments: "Very useful",
    tags: ["challenging", "good-examples"],
    submitted_at: new Date(),
    attachments: [{ filename: "lab.pdf", size_kb: 180 }]
  }
])


// 5. Insert Second Batch of Documents
db.feedback.insertMany([
  {
    student_id: 3,
    course_code: "CS101",
    semester: "2022-ODD",
    rating: 3,
    comments: "Course content was average",
    tags: ["difficult"],
    submitted_at: new Date(),
    attachments: [{ filename: "assignment_notes.pdf", size_kb: 120 }]
  },
  {
    student_id: 4,
    course_code: "CS102",
    semester: "2022-EVEN",
    rating: 5,
    comments: "Database topics were explained clearly",
    tags: ["interesting", "well-structured"],
    submitted_at: new Date(),
    attachments: [{ filename: "db_reference.pdf", size_kb: 200 }]
  },
  {
    student_id: 5,
    course_code: "CS102",
    semester: "2022-ODD",
    rating: 2,
    comments: "More examples would be helpful",
    tags: ["hard"],
    submitted_at: new Date(),
    attachments: [{ filename: "course_review.pdf", size_kb: 90 }]
  },
  {
    student_id: 6,
    course_code: "EC101",
    semester: "2021-EVEN",
    rating: 1,
    comments: "Concepts were difficult to understand",
    tags: ["confusing"],
    submitted_at: new Date(),
    attachments: [{ filename: "feedback_note.pdf", size_kb: 60 }]
  },
  {
    student_id: 7,
    course_code: "ME101",
    semester: "2022-ODD",
    rating: 4,
    comments: "Practical sessions were useful",
    tags: ["practical"],
    submitted_at: new Date(),
    attachments: [{ filename: "mechanics_notes.pdf", size_kb: 110 }]
  },
  {
    student_id: 8,
    course_code: "CS103",
    semester: "2022-ODD",
    rating: 5,
    comments: "Object-oriented concepts were interesting",
    tags: ["interesting", "good-examples"],
    submitted_at: new Date(),
    attachments: [{ filename: "oop_material.pdf", size_kb: 150 }]
  },
  {
    student_id: 9,
    course_code: "EC101",
    semester: "2022-ODD",
    rating: 2,
    comments: "Needs better explanation",
    tags: ["hard"],
    submitted_at: new Date()
  },
  {
    student_id: 10,
    course_code: "CS101",
    semester: "2022-ODD",
    rating: 5,
    comments: "One of my favorite subjects",
    tags: ["challenging", "good-examples"],
    submitted_at: new Date(),
    attachments: [{ filename: "cs_notes.pdf", size_kb: 140 }]
  }
])


// 6. Read - Find all documents
db.feedback.find()


// 7. Count total documents
db.feedback.countDocuments()


// 8. Find documents with rating = 5
db.feedback.find({ rating: 5 })


// 9. Find with multiple conditions (CS101 + challenging tag)
db.feedback.find({
  course_code: "CS101",
  tags: "challenging"
})


// 10. Projection - Show only student_id, course_code, rating
db.feedback.find(
  {},
  { student_id: 1, course_code: 1, rating: 1, _id: 0 }
)


// 11. Update - Add needs_review flag for low ratings (< 3)
db.feedback.updateMany(
  { rating: { $lt: 3 } },
  { $set: { needs_review: true } }
)


// 12. Update - Push "reviewed" tag to needs_review documents
db.feedback.updateMany(
  { needs_review: true },
  { $push: { tags: "reviewed" } }
)


// 13. Delete - Remove documents from 2021-EVEN semester
db.feedback.deleteMany({
  semester: "2021-EVEN"
})


// 14. Aggregation - Average rating per course (2022-ODD semester)
db.feedback.aggregate([
  { $match: { semester: "2022-ODD" } },
  {
    $group: {
      _id: "$course_code",
      avg_rating: { $avg: "$rating" },
      total_feedback: { $sum: 1 }
    }
  },
  { $sort: { avg_rating: -1 } }
])


// 15. Aggregation - With $project to rename fields and round rating
db.feedback.aggregate([
  { $match: { semester: "2022-ODD" } },
  {
    $group: {
      _id: "$course_code",
      avg_rating: { $avg: "$rating" },
      total_feedback: { $sum: 1 }
    }
  },
  {
    $project: {
      _id: 0,
      course_code: "$_id",
      average_rating: { $round: ["$avg_rating", 1] },
      total_feedback: 1
    }
  },
  { $sort: { average_rating: -1 } }
])


// 16. Aggregation - Tag frequency using $unwind
db.feedback.aggregate([
  { $unwind: "$tags" },
  {
    $group: {
      _id: "$tags",
      count: { $sum: 1 }
    }
  },
  { $sort: { count: -1 } }
])


// 17. Create Index on course_code
db.feedback.createIndex({ course_code: 1 })


// 18. Explain query to verify index usage
db.feedback.find({
  course_code: "CS101"
}).explain("executionStats")