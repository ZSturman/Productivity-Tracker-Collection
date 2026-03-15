//
//  ModelTests.swift
//  WellTrackTests
//
//  Created by Zachary Sturman on 8/15/23.
//

import XCTest
@testable import WellTrack

final class ModelTests: XCTestCase {
    
    private var controller: ActionStateDataController!
    
    
    override func setUp() {
        controller = .shared
    }
    
    // Everytime we run a new test we run it with a new DataController
    override func tearDown() {
        controller = nil
    }
    
    func testActionStateIsEmpty() {
        let actionState = ActionState.empty(context: controller.viewContext)
        XCTAssertEqual(actionState.title, "")
        
        XCTAssertTrue(actionState.collectLocation)
        
        XCTAssertTrue(Calendar.current.isDateInToday(actionState.dateCreated))
        XCTAssertTrue(Calendar.current.isDateInToday(actionState.dateUpdated))
    }
    
    func testActionStateIsNotValid() {
        let actionState = ActionState.empty(context: controller.viewContext)
        
        XCTAssertFalse(actionState.isValid)
    }
    
    func testActionStateIsValid() {
        let actionState = ActionState.preview(context: controller.viewContext)
        XCTAssertTrue(actionState.isValid)
    }
    
    func testMakeActionStatePreviewIsValid() {
        
        let count = 10
        let actionStates = ActionState.makePreview(count: count, in: controller.viewContext)
        for i in 0..<actionStates.count {
            let actionState = actionStates[i]
            XCTAssertEqual(actionState.title, "ActionState \(i)")
            
            XCTAssertNotNil(actionState.collectLocation)
        }
    }
    
    func testFilterCollectLocaleRequestIsValid() {
        let request = ActionState.filter(with: .init(filter: .collectLocale))
        XCTAssertEqual("collectLocation == 1", request.predicateFormat)
    }
    
    func testFilterAllActionStatesRequestIsValid() {
        let request = ActionState.filter(with: .init(filter: .all))
        XCTAssertEqual("TRUEPREDICATE", request.predicateFormat)
    }
    
    func testFilterAllWithQueryRequestIsValid() {
        let query = "xyz"
        let request = ActionState.filter(with: .init(query: query))
        XCTAssertEqual("title CONTAINS[cd] \"\(query)\"", request.predicateFormat)
    }
    
    func testFilterCollectLocaleWithQueryRequestIsValid() {
        let query = "xyz"
        let request = ActionState.filter(with: .init(query: query, filter: .collectLocale))
        let actualPredicate = request.predicateFormat
        XCTAssertEqual(actualPredicate, "title CONTAINS[cd] \"\(query)\" AND collectLocation == 1", "Expected different predicate. Got: \(actualPredicate)")
    }


    
    

    func testExample() throws {
        // This is an example of a functional test case.
        // Use XCTAssert and related functions to verify your tests produce the correct results.
        // Any test you write for XCTest can be annotated as throws and async.
        // Mark your test throws to produce an unexpected failure when your test encounters an uncaught error.
        // Mark your test async to allow awaiting for asynchronous code to complete. Check the results with assertions afterwards.
    }

    func testPerformanceExample() throws {
        // This is an example of a performance test case.
        self.measure {
            // Put the code you want to measure the time of here.
        }
    }

}
